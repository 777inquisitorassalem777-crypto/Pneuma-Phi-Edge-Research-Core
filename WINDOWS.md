# Запуск на Windows

## Вариант 1 — без сборки (рекомендуется для разработки)

1. Установите [Python 3.10+](https://www.python.org/downloads/)  
   (отметьте **Add python.exe to PATH**).
2. Распакуйте архив.
3. Дважды щёлкните:

```
scripts\run.bat
```

или в PowerShell:

```powershell
.\scripts\run.ps1
.\scripts\run.ps1 --mode archetypal --steps 60 --scenario stress
```

## Вариант 2 — собрать EXE

На **Windows**-машине с Python:

```bat
scripts\build_exe.bat
```

Готовый файл:

```
dist\PNEUMA-Symbiosis.exe
```

Запуск:

```bat
PNEUMA-Symbiosis.exe
PNEUMA-Symbiosis.exe --mode archetypal --steps 80 --scenario stress --export out.json
```

> Сборка EXE выполняется **на Windows**. В Linux-среде разработчика получается не Windows PE, а ELF.  
> `build_exe.bat` использует PyInstaller one-file.

## Вариант 3 — через spec

```bat
.venv\Scripts\activate
pip install pyinstaller
pyinstaller pneuma.spec
```

## Требования

- Windows 10/11 x64
- Python 3.10+ (только для bat/ps1 и для сборки EXE)
- После сборки EXE Python на целевой машине **не обязателен**
