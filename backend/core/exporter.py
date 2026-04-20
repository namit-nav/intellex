def export_markdown(filename, content):

    with open(filename, "w") as f:
        f.write("# AI Research Report\n\n")
        f.write(content)

    print(f"\nReport saved as {filename}")