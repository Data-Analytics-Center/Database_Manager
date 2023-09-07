"""small test file."""

import pandas as pd

MAX_INSERT_LIMIT = 80000

def main():
    """Main function."""  # noqa: D401
    ids = [i for i in range(MAX_INSERT_LIMIT )]
    vals = [f"val_{i}" for i in range(MAX_INSERT_LIMIT)]

    data_frame = pd.DataFrame({"id": ids, "val": vals})
    print(data_frame)

if __name__ == "__main__":
    main()