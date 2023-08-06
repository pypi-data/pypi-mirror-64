import ray
import argparse
from ray.streaming import StreamingContext


def wordcount_v3():
    import os
    os.environ['GRPC_VERBOSITY'] = 'DEBUG'
    os.environ['GRPC_TRACE'] = 'tcp'
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--titles-file",
        required=True,
        help="the file containing the wikipedia titles to lookup")
    args = parser.parse_args()
    titles_file = str(args.titles_file)
    ray.init(load_code_from_local=True, include_java=False)
    ctx = StreamingContext.Builder() \
        .build()
    ctx.read_text_file(titles_file) \
        .set_parallelism(1) \
        .flat_map(lambda x: x.split()) \
        .map(lambda x: (x, 1)) \
        .key_by(lambda x: x[0]) \
        .reduce(lambda old_value, new_value:
                (old_value[0], old_value[1] + new_value[1])) \
        .filter(lambda x: "ray" not in x) \
        .sink(lambda x: print("result", x))
    ctx.submit("word_count")
    import time
    time.sleep(3)
    ray.shutdown()


if __name__ == "__main__":
    wordcount_v3()
