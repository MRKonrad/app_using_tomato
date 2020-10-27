from conans import ConanFile, CMake, tools


class TomatoConan(ConanFile):
    name = "tomato"
    version = "0.5"
    license = "<Put the package license here>"
    author = "MRKonrad"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<CMR map calculation library>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "CMAKE_C_COMPILER": "ANY", "CMAKE_CXX_COMPILER": "ANY"}
    default_options = {"shared": False, "CMAKE_C_COMPILER": None, "CMAKE_CXX_COMPILER": None}
    generators = "cmake"

    def source(self):
        self.run("git clone --recursive https://github.com/MRKonrad/tomato.git --branch conan")

        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("tomato/CMakeLists.txt", "project(Tomato)",
                              '''PROJECT(tomato)
                              include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
                              conan_basic_setup(KEEP_RPATHS)''')

    def _configure_cmake(self):
        cmake = CMake(self)

        # set compiler path, this option is included for
        # MACOS & using older clang version than the system one
        # older clang version can be installed using macports
        # https://ports.macports.org/port/clang-10/summary
        if self.options.CMAKE_C_COMPILER:
            cmake.definitions["CMAKE_C_COMPILER"] = self.options.CMAKE_C_COMPILER
        if self.options.CMAKE_CXX_COMPILER:
            cmake.definitions["CMAKE_CXX_COMPILER"] = self.options.CMAKE_CXX_COMPILER

        if (tools.os_info.is_macos):
            cmake.definitions["CMAKE_MACOSX_RPATH"] = "ON"

        if (tools.os_info.is_linux):
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"

        # Windows and shared libs
        if (tools.os_info.is_windows):
            cmake.definitions["CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS"] = "ON"

        cmake.configure(source_folder="tomato")
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["TomatoLib"]
