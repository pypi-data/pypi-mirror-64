import os
from assnake.core.result import Result

this_dir = os.path.dirname(os.path.abspath(__file__))
result = Result.from_location(name = 'count', location = this_dir, input_type = 'illumina_strand_file', additional_inputs = None)

