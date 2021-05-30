class FileVisitResult:
    pass

FileVisitResult.CONTINUE
FileVisitResult.TERMINATE
FileVisitResult.SKIP_SUBTREE
FileVisitResult.SKIP_SIBLINGS


class FileVisitor:
    pass

def pre_visit_directory(dir):
    pass

def visit_file(file):
    pass

def visit_file_failed(file):
    pass

def post_visit_directory(dir):
    pass

Path startig_dir = Paths.get("pathToDir")
FileVisitorImpl visitor = new FileVisitorImpl()
Files.walkFileTree(startingDir, visitor)


