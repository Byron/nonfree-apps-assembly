#-*-coding:utf-8-*-
"""
@package bprocess-delegate
@brief Plugins for the bprocess framework

@author Sebastian Thiel
@copyright [MIT License](http://www.opensource.org/licenses/mit-license.php)
"""
from __future__ import unicode_literals
from butility.future import str

from bprocess import ProcessControllerDelegate

class MayaProcessControllerDelegate(ProcessControllerDelegate):
    """Customize behaviour to better deal with path-related variables used in maya"""
    __slots__ = ()
    
    context_from_path_arguments = True

    def verify_path(self, environment_variable, path):
        """Deals properly with icon-paths, those are only relevant on linux"""
        if not path.endswith('%B'):
            return super(MayaProcessControllerDelegate, self).verify_path(environment_variable, path)
        # end see if path is a linux iconpath
        
        # If the base does not exist, its invalid. Otherwise we just return it unchanged
        checked_path = super(MayaProcessControllerDelegate, self).verify_path(environment_variable, path.dirname())
        if checked_path is None:
            return None
        return path

# end class MayaProcessControllerDelegate


class KatanaProcessControllerDelegate(ProcessControllerDelegate):
    """Assure we understand the Katana Resource Path as path"""
    __slots__ = ()
    
    def variable_is_path(self, environment_variable):
        """Handle Katana Resources """
        if environment_variable in ('KATANA_RESOURCES', 'KATANA_RESOLUTIONS'):
            return True
        return super(KatanaProcessControllerDelegate, self).variable_is_path(environment_variable)
        
    def variable_is_appendable(self, environment_variable, value):
        """Implements Katana specific special cases"""
        res = super(KatanaProcessControllerDelegate, self).variable_is_appendable(environment_variable, value)
        return environment_variable != 'KATANA_RESOLUTIONS' and res

# end class KatanaProcessControllerDelegate


class MariProcessControllerDelegate(ProcessControllerDelegate):
    """A controller to ease starting Mari with all it's peculiarities"""
    __slots__ = ()

    def pre_start(self, executable, env, args, cwd, resolve):
        """Prevent the browser to be shown"""
        args.insert(0, '--nobrowser')
        return super(MariProcessControllerDelegate, self).pre_start(executable, env, args, cwd, resolve)

# end class MariProcessControllerDelegate


class ThreeDEqualizerProcessControllerDelegate(ProcessControllerDelegate):
    """Make sure custom path variables are handled correctly"""
    __slots__ = ()

    def variable_is_path(self, environment_variable):
        res = super(ThreeDEqualizerProcessControllerDelegate, self).variable_is_path(environment_variable)
        if res:
            return res
        evar = environment_variable.lower()
        return 'python_custom' in evar or evar.endswith('_dir')

# end class ThreeDEqualizerProcessControllerDelegate
