class Task:
    def __init__(self, program_suite, program_name, file_path, main_function, oracle_path, oracle_main, headers_path):
        self.program_suite = program_suite
        self.program_name = program_name
        self.headers_path = headers_path
        self.file_path = file_path
        self.main_function = main_function
        self.oracle_path = oracle_path
        self.oracle_main = oracle_main
