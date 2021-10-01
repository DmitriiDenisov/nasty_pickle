source = """
a=3\n
if a<4:\n
    print("a<4")\n
else:\n
    print("a>=4")\n
for i in range(1, 10):\n
    print(f"Current i:{i}")\n"""
exec(source)
