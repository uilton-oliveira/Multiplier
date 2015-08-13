def remove_comments(filepath, tmp):
    file1 = open(filepath, 'r')
    fcontent = file1.read()
    file1.close()
    fresult = ''
    for line in fcontent.split('\n'):
        if line.lstrip().startswith('/'):
            continue
        if '//' in line:
            line = line.split('/')[0]
        fresult += line + '\n'
    file1.close()
    file1 = open(tmp, 'w')
    file1.write(fresult)
    file1.close()
