def view_products(products):
    print("\nID | NOME | QUANTIDADE | PREÇO UNITÁRIO")
    print("-" * 50)
    for p in products:
        print(
            f"{p[0]} | {p[1]} | {p[2]} UN | R$ {(f'{p[3]:.2f}').replace('.', ',')}")
    print("-" * 50)
