#!/usr/bin/env python3
import os
from datetime import datetime

def generate_tree(startpath, excluded_dirs, excluded_files, output_filename, excluded_extensions):
    """
    Generuje PEŁNĄ strukturę drzewa katalogów, oznaczając pliki pominięte przy kopiowaniu.
    """
    tree_lines = [f"Drzewo projektu (wygenerowano: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})", "="*40]
    
    excluded_extensions_set = set(excluded_extensions)
    excluded_files_set = set(excluded_files)

    for root, dirs, files in os.walk(startpath, topdown=True):
        dirs[:] = [d for d in dirs if d not in excluded_dirs and not d.startswith('.')]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        
        # Wyświetlanie nazwy katalogu
        if level == 0:
            # POPRAWKA: Używamy 'startpath' zamiast 'project_dir'
            tree_lines.append(f"{os.path.basename(startpath)}/")
        else:
            tree_lines.append(f"{indent}└── {os.path.basename(root)}/")

        subindent = ' ' * 4 * (level + 1)
        
        display_files = sorted([f for f in files if not f.startswith('.') and f != output_filename])

        for i, f in enumerate(display_files):
            connector = "└──" if i == len(display_files) - 1 else "├──"
            
            is_skipped = any(f.endswith(ext) for ext in excluded_extensions_set) or f in excluded_files_set
            annotation = "  (pominięty)" if is_skipped else ""
            
            tree_lines.append(f"{subindent}{connector} {f}{annotation}")
                
    return "\n".join(tree_lines)


def copy_project_files_to_single_file(project_dir, output_file):
    """
    Kopiuje zawartość plików tekstowych projektu do jednego pliku, dodając nagłówki 
    i PEŁNE drzewo katalogów na końcu.
    """
    # --- Konfiguracja Wykluczeń ---
    excluded_dirs = [
        'venv', '__pycache__', 'migrations', '.git', 'node_modules', 
        '.vscode', '.idea', 'build', 'dist', 'media', 'assets'
    ]
    excluded_files = [
        '.env', 'db.sqlite3', '.DS_Store'
    ]
    excluded_extensions = [
        '.pyc', '.log', '.bak', '.tmp', '.swp', '.db', '.sqlite3', '.png', '.jpg', 
        '.jpeg', '.gif', '.bmp', '.ico', '.webp', '.svg', '.tif', '.tiff', '.woff', 
        '.woff2', '.ttf', '.otf', '.eot', '.mp3', '.wav', '.ogg', '.mp4', '.mov', 
        '.avi', '.mkv', '.zip', '.rar', '.gz', '.tar', '.7z', '.pdf', '.doc', 
        '.docx', '.xls', '.xlsx', '.exe', '.dll', '.so', '.bin'
    ]

    project_dir = os.path.expanduser(project_dir)
    output_file = os.path.expanduser(output_file)
    output_filename = os.path.basename(output_file)

    files_to_process = []
    
    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in excluded_dirs and not d.startswith('.')]
        
        for file in files:
            if file == output_filename or file.startswith('.') or file in excluded_files:
                continue
            if any(file.endswith(ext) for ext in excluded_extensions):
                continue
            file_path = os.path.join(root, file)
            files_to_process.append(file_path)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(f"Połączona zawartość projektu: {os.path.basename(project_dir)}\n")
        outfile.write(f"Wygenerowano: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        outfile.write(f"Liczba przetworzonych plików tekstowych: {len(files_to_process)}\n")
        outfile.write("\n" + "="*80 + "\n\n")

        for file_path in sorted(files_to_process):
            relative_path = os.path.relpath(file_path, project_dir)
            header = f"""#####################################
#
# Plik: {relative_path.replace(os.sep, '/')}
#
#####################################\n\n"""
            outfile.write(header)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    outfile.write(content)
            except UnicodeDecodeError:
                outfile.write(f"--- UWAGA: Plik '{relative_path}' nie mógł zostać odczytany jako tekst ---")
            except Exception as e:
                outfile.write(f"Błąd podczas odczytu pliku {file_path}: {e}")
            
            outfile.write("\n\n" + "="*80 + "\n\n")
        
        outfile.write("\n\n" + "="*30 + " STRUKTURA PROJEKTU " + "="*30 + "\n\n")
        project_tree = generate_tree(project_dir, excluded_dirs, excluded_files, output_filename, excluded_extensions)
        outfile.write(project_tree)
        outfile.write("\n\n" + "="*80 + "\n")

    print(f"Projekt został pomyślnie zapisany do pliku: {output_file}")


# --- Uruchomienie skryptu ---
project_directory = '~/kagyu_mini_cms'
output_file_path = '~/kagyu_mini_cms/combined_project_files.txt'
copy_project_files_to_single_file(project_directory, output_file_path)