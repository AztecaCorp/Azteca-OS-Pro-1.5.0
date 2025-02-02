from cx_Freeze import setup, Executable

# Define your game script name
script_name = "main.py"  # Change this to your script name

# Include any additional files like images, sounds, etc.
include_files = [
    "kill_sound.wav",
    "death_sound.wav",
    "level_up_sound.wav",

]

# Define the setup
setup(
    name="Space Fight 2",
    version="0.1",
    description="Space Fight Azteca Games",
    options={
        "build_exe": {
            "include_files": include_files,
        }
    },
    executables=[Executable(script_name)],
)
