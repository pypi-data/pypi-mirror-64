try:
#import os
#packagedir = os.path.dirname(__file__)
#from .annotator_options import AnnotatorOptions
#from .inout import CravatReader
#from .inout import CravatWriter
#from .inout import ColumnDefinition
    from .base_converter import BaseConverter
    from .base_annotator import BaseAnnotator
    from .base_mapper import BaseMapper
    from .base_postaggregator import BasePostAggregator
    from .cravat_report import CravatReport
    from .exceptions import *
    from . import util
    from . import admin_util
    from .config_loader import ConfigLoader
    from . import constants
    from .cravat_filter import CravatFilter
#from .store_utils import ProgressStager
#from .webresult.webresult import *
#from .webstore.webstore import *
    from .cravat_class import Cravat
    from .util import get_ucsc_bins, reverse_complement, translate_codon, more_severe_so, switch_strand
    from .constants import crx_def
except KeyboardInterrupt:
    import sys
    sys.exit(1)

def get_live_annotator (module_name):
    import os
    config_loader = ConfigLoader()
    script_path = admin_util.get_annotator_script_path(module_name)
    ModuleClass = util.load_class('CravatAnnotator', script_path)
    module = ModuleClass(None, None, live=True)
    try:
        module.annotator_name = module_name
        module.annotator_dir = os.path.dirname(script_path)
        module.data_dir = os.path.join(module.annotator_dir, 'data')
        module._open_db_connection()
        module.conf = config_loader.get_module_conf(module_name)
        module.setup()
    except:
        print('    module loading error: {}'.format(module.annotator_name))
        return None
    return module

def get_live_mapper (module_name):
    import os
    config_loader = ConfigLoader()
    script_path = admin_util.get_mapper_script_path(module_name)
    ModuleClass = util.load_class('Mapper', script_path)
    module = ModuleClass(None, None, live=True)
    try:
        module.module_name = module_name
        module.mapper_dir = os.path.dirname(script_path)
        module.data_dir = os.path.join(module.mapper_dir, 'data')
        module.conf = config_loader.get_module_conf(module_name)
        module.setup()
    except Exception as e:
        print('    module loading error: {}'.format(module_name))
        return None
    return module
