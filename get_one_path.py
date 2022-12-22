import os


def get_next(mark: int, id: int) -> str:
    """Returns next filename

    Args:
        mark (int): Class ID
        id (int): File ID
        
    Returns:
        str: Path to propper file
    """
    return os.path.abspath("..\\first_lab\\dataset"+f'\\{mark}'+f'\\{id:04}.txt')


if __name__ == "__main__":
    mark = 4
    path_to_dataset = os.path.abspath("../application_programming_first_lab_and_dataset/dataset")
    folder_path = path_to_dataset + f'/{mark}'

    num_of_files = sum(os.path.isfile(os.path.join(folder_path, f))
                       for f in os.listdir(folder_path)) + 1

    for id in range(1, num_of_files):
        print(get_next(mark, id))