from pathlib import Path

a = Path(__file__)
print('\\backend\\' in f'{a.absolute()}')
print(r"\back\")
