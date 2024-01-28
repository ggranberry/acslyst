class Task:
    def __init__(
        self,
        program_suite,
        program_name,
        program_file,
        main_function,
        oracle_file,
        oracle_main,
        headers_path,
        timestamp,
        parameters_file,
        annotated_programs_output_dir,
    ):
        self.timestamp = timestamp
        self.program_suite = program_suite
        self.program_name = program_name
        self.headers_path = headers_path
        self.program_file= program_file 
        self.main_function = main_function
        self.oracle_file= oracle_file 
        self.oracle_main = oracle_main
        self.parameters_file = parameters_file
        self.annotated_programs_output_dir=annotated_programs_output_dir
