import os


class Iterator:
    def __init__(self, name_of_file):
        self.name_of_file = name_of_file
        self.counter = 0
        self.list = []
        file = open(self.name_of_file, "r")
        for row in file:
            self.list.append(row)
        file.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter < len(self.list):
            tmp = self.list[self.counter]
            self.counter += 1
            return tmp
        else:
            raise StopIteration


if __name__ == "__main__":
    mark = 4
    path_to_dataset = os.path.abspath("../application_programming_first_lab_and_dataset/dataset")
    folder_path = path_to_dataset + f'/{mark}'

    num_of_files = sum(os.path.isfile(os.path.join(folder_path, f))
                       for f in os.listdir(folder_path)) + 1

    iter = Iterator(num_of_files, mark, folder_path)
