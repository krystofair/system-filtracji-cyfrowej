from platform import architecture as arch
from functools import reduce
from kivy.properties import DictProperty, ObjectProperty


class NotLoadedProfileException(Exception):
    def __init__(self):
        super().__init__("Profile is not Loaded")


class Profile:
    """Interface for guide what properties will be passed in 100% to filter during generation."""
    s_points = DictProperty()  # points on chart which are updating during modifying line.
    interp_func = ObjectProperty()  # Method of interpolation of s_points

    def __init__(self):
        self.byte_len = 4 if arch()[0] == "32bit" else 8
        self.loaded = False

    def get_points_as_list(self):
        tmp_points = list(self.s_points.items())
        tmp_points.sort(key=lambda x: x[0])
        return tmp_points

    def save_profile(self, path):
        if not self.loaded:
            raise NotLoadedProfileException
        out_file = open(path, 'wb')
        out_file.write(b'CHR4' if self.byte_len == 4 else b'CHR8')
        out_file.write(len(self.s_points).to_bytes(self.byte_len, 'little'))
        out_file.write(
            bytes().join(map(lambda x: x.to_bytes(self.byte_len, 'little'),
                             reduce(lambda x, y: x + [y[0], y[1]], self.s_points, []))))
        out_file.close()

    def load_profile(self, path):
        """throws exception(ValueError, EOFError), when loading file failed"""
        # TODO: zoptymalizować wczytywanie, bo może nie być wydajne
        in_file = open(path, 'rb')
        if in_file.read(3) != b'CHR':
            in_file.close()
            raise ValueError("That is not file of profile.")
        try:
            #TODO: To be certain that loading is in little endian.
            self.byte_len = int(in_file.read(1), 10)
            if self.byte_len != 4 and self.byte_len != 8:
                raise ValueError("Byte's length was wrong number.")
            count_of_points = int(in_file.read(self.byte_len), 10)
            for pc in range(count_of_points):
                x = int(in_file.read(self.byte_len), 10)
                y = int(in_file.read(self.byte_len), 10)
                self.s_points.update({x: y})
        except EOFError:
            print("There was unexpected end of file.")
        except Exception as e:
            print(e)
            raise e
        finally:
            in_file.close()
        self.loaded = True
