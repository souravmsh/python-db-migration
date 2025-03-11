import time
import datetime

"""_summary_
    from utils.benchmark import benchmark
    
    # Test Benchmark 1
    benchmark.start("MyBenchmark1")
    benchmark.progress("MyBenchmark1")
    benchmark.end("MyBenchmark1")
    
    # Test Benchmark 2
    benchmark.start("MyBenchmark2")
    benchmark.progress("MyBenchmark2")
    benchmark.end("MyBenchmark2")
"""

class Benchmark:
    
    def __init__(self):
        self.start_times = {}
        self.start_timestamps = {}
        self.end_times = {}
        self.end_timestamps = {}
        self.progress_times = {}
    
    def start(self, benchmark_point="benchmark_start_point"):
        self.start_times[benchmark_point] = time.perf_counter()
        self.start_timestamps[benchmark_point] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f"benchmark#{benchmark_point} started at {self.start_timestamps[benchmark_point]}"
    
    def progress(self, benchmark_point):
        if benchmark_point in self.start_times:
            elapsed_time = time.perf_counter() - self.start_times[benchmark_point]
            self.progress_times[benchmark_point] = elapsed_time
            return f"benchmark#{benchmark_point} progress in {elapsed_time:.6f} seconds at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        return f"Benchmark point '{benchmark_point}' not found. Start it first."
    
    def end(self, benchmark_point):
        if benchmark_point in self.start_times:
            self.end_times[benchmark_point] = time.perf_counter()
            self.end_timestamps[benchmark_point] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            elapsed_time = self.end_times[benchmark_point] - self.start_times[benchmark_point]
            return f"benchmark#{benchmark_point} finished at {self.end_timestamps[benchmark_point]} after {elapsed_time:.6f} seconds"
        return f"Benchmark point '{benchmark_point}' not found. Start it first."


# Example usage
benchmark = Benchmark()