from flask import Flask, render_template, request, redirect,session
import sqlite3

app = Flask(__name__)
app.secret_key="inventorysecret"

def get_db():
    return sqlite3.connect("database.db")


'''@app.route("/")  
def home():
    return render_template("base.html")'''


@app.route("/suppliers", methods=["GET", "POST"])
def suppliers():
    con = get_db()
    cur = con.cursor()

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        cur.execute("INSERT INTO suppliers(name, phone) VALUES (?,?)", (name, phone))
        con.commit()

    cur.execute("SELECT * FROM suppliers")
    data = cur.fetchall()
    con.close()

    return render_template("suppliers.html", suppliers=data)


@app.route("/delete_supplier/<int:id>")
def delete_supplier(id):

    con = get_db()
    cur = con.cursor()

    cur.execute(
        "DELETE FROM suppliers WHERE id=?",
        (id,)
    )

    con.commit()
    con.close()

    return redirect("/suppliers") 


@app.route("/edit_supplier/<int:id>", methods=["GET", "POST"])
def edit_supplier(id):

    con = get_db()
    cur = con.cursor()

    # UPDATE SUPPLIER
    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]

        cur.execute("""
            UPDATE suppliers
            SET name=?, phone=?
            WHERE id=?
        """, (name, phone, id))

        con.commit()

        return redirect("/suppliers")

    # FETCH SUPPLIER
    cur.execute("""
        SELECT *
        FROM suppliers
        WHERE id=?
    """, (id,))

    supplier = cur.fetchone()

    con.close()

    return render_template(
        "edit_supplier.html",
        supplier=supplier
    )
    
        
@app.route("/warehouses", methods=["GET", "POST"])
def warehouses():
    con = get_db()
    cur = con.cursor()

    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]
        cur.execute("INSERT INTO warehouses(name, location) VALUES (?,?)", (name, location))
        con.commit()

    cur.execute("SELECT * FROM warehouses")
    data = cur.fetchall()
    con.close()

    return render_template("warehouses.html", warehouses=data)


@app.route("/delete_warehouse/<int:id>")
def delete_warehouse(id):

    con = get_db()
    cur = con.cursor()

    cur.execute(
        "DELETE FROM warehouses WHERE id=?",
        (id,)
    )

    con.commit()
    con.close()

    return redirect("/warehouses")

@app.route("/edit_warehouse/<int:id>", methods=["GET", "POST"])
def edit_warehouse(id):

    con = get_db()
    cur = con.cursor()

    if request.method == "POST":

        name = request.form["name"]
        location = request.form["location"]

        cur.execute("""
            UPDATE warehouses
            SET name=?, location=?
            WHERE id=?
        """, (name, location, id))

        con.commit()

        return redirect("/warehouses")

    cur.execute("""
        SELECT *
        FROM warehouses
        WHERE id=?
    """, (id,))

    warehouse = cur.fetchone()

    con.close()

    return render_template(
        "edit_warehouse.html",
        warehouse=warehouse
    )        

#  Adding or getting CUSTOMERS 
@app.route("/customers", methods=["GET", "POST"])
def customers():
    con = get_db()
    cur = con.cursor()

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        address = request.form["address"]

        cur.execute("""
        INSERT INTO customers(name, phone, email, address)
        VALUES (?,?,?,?)
        """, (name, phone, email, address))
        con.commit()

    cur.execute("SELECT * FROM customers")
    data = cur.fetchall()
    con.close()

    return render_template("customers.html", customers=data)

@app.route("/delete_customer/<int:id>")
def delete_customer(id):
    con = get_db()
    cur = con.cursor()
    cur.execute("DELETE FROM customers WHERE id=?", (id,))
    con.commit()
    con.close()
    return redirect("/customers")    

@app.route("/edit_customer/<int:id>", methods=["GET", "POST"])
def edit_customer(id):

    con = get_db()
    cur = con.cursor()

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        address = request.form["address"]

        cur.execute("""
        UPDATE customers
        SET name=?, phone=?, email=?, address=?
        WHERE id=?
        """, (name, phone, email, address, id))

        con.commit()

        return redirect("/customers")

    cur.execute("SELECT * FROM customers WHERE id=?", (id,))
    customer = cur.fetchone()

    con.close()

    return render_template(
        "edit_customer.html",
        customer=customer
    )   

#updated
# - PRODUCTS 
@app.route("/products", methods=["GET", "POST"])
def products():

    con = get_db()
    cur = con.cursor()

    # ADD PRODUCT
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        qty = request.form["qty"]
        supplier = request.form["supplier"]
        warehouse = request.form["warehouse"]

        cur.execute("""
        INSERT INTO products(name, price, qty, supplier_id, warehouse_id)
        VALUES (?,?,?,?,?)
        """, (name, price, qty, supplier, warehouse))
        con.commit()

    # SEARCH
    search = request.args.get("search")

    if search:
        cur.execute("""
        SELECT p.id, p.name, p.price, p.qty,
               s.name, w.name
        FROM products p
        LEFT JOIN suppliers s ON p.supplier_id=s.id
        LEFT JOIN warehouses w ON p.warehouse_id=w.id
        WHERE p.name LIKE ?
        """, ('%' + search + '%',))
    else:
        cur.execute("""
        SELECT p.id, p.name, p.price, p.qty,
               s.name, w.name
        FROM products p
        LEFT JOIN suppliers s ON p.supplier_id=s.id
        LEFT JOIN warehouses w ON p.warehouse_id=w.id
        """)

    products = cur.fetchall()

    # dropdown data
    cur.execute("SELECT id, name FROM suppliers")
    suppliers = cur.fetchall()

    cur.execute("SELECT id, name FROM warehouses")
    warehouses = cur.fetchall()

    con.close()

    return render_template("products.html",
                           suppliers=suppliers,
                           warehouses=warehouses,
                           products=products)

 # DELETE PRODUCT 
@app.route("/delete_product/<int:id>")
def delete_product(id):
    con = get_db()
    cur = con.cursor()
    cur.execute("DELETE FROM products WHERE id=?", (id,))
    con.commit()
    con.close()
    return redirect("/products")

@app.route("/edit_product/<int:id>", methods=["GET","POST"])
def edit_product(id):
    con = get_db()
    cur = con.cursor()

    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        qty = request.form["qty"]

        cur.execute(
            "UPDATE products SET name=?, price=?, qty=? WHERE id=?",
            (name, price, qty, id)
        )
        con.commit()
        return redirect("/products")

    cur.execute("SELECT * FROM products WHERE id=?", (id,))
    product = cur.fetchone()
    con.close()

    return render_template("edit_product.html", product=product)    

'''@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    con = get_db()
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM products")
    total_products = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM products WHERE qty < 5")
    low_stock = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM suppliers")
    total_suppliers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM customers")
    total_customers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM warehouses")
    total_warehouses = cur.fetchone()[0]

    con.close()

    return render_template(
        "dashboard.html",
        total_products=total_products,
        low_stock=low_stock,
        total_suppliers=total_suppliers,
        total_customers=total_customers,
        total_warehouses=total_warehouses
    ) '''

@app.route("/dashboard")
def dashboard():

    # Check login
    if "user" not in session:
        return redirect("/")

    con = get_db()
    cur = con.cursor()

    # =========================
    # SALES & PURCHASES
    # =========================

    # Total Sales
    cur.execute("SELECT SUM(total) FROM sales")
    total_sales = cur.fetchone()[0] or 0

    # Total Purchases
    cur.execute("SELECT SUM(total) FROM purchases")
    total_purchases = cur.fetchone()[0] or 0

    # Profit Calculation
    profit = total_sales - total_purchases

    # =========================
    # PRODUCT STATISTICS
    # =========================

    # Total Products
    cur.execute("SELECT COUNT(*) FROM products")
    total_products = cur.fetchone()[0]

    # Low Stock Products
    cur.execute("SELECT COUNT(*) FROM products WHERE qty < 5")
    low_stock = cur.fetchone()[0]

    # =========================
    # BUSINESS RECORDS
    # =========================

    # Total Customers
    cur.execute("SELECT COUNT(*) FROM customers")
    total_customers = cur.fetchone()[0]

    # Total Suppliers
    cur.execute("SELECT COUNT(*) FROM suppliers")
    total_suppliers = cur.fetchone()[0]

    # Total Warehouses
    cur.execute("SELECT COUNT(*) FROM warehouses")
    total_warehouses = cur.fetchone()[0]

    # =========================
    # TOP SELLING PRODUCT
    # =========================

    cur.execute("""
        SELECT p.name, SUM(s.qty) as total_qty
        FROM sales s
        JOIN products p
        ON s.product_id = p.id
        GROUP BY p.name
        ORDER BY total_qty DESC
        LIMIT 1
    """)

    top_product = cur.fetchone()

    con.close()

    return render_template(
        "dashboard.html",

        # Sales
        total_sales=total_sales,
        total_purchases=total_purchases,
        profit=profit,

        # Products
        total_products=total_products,
        low_stock=low_stock,

        # Business Data
        total_customers=total_customers,
        total_suppliers=total_suppliers,
        total_warehouses=total_warehouses,

        # Analytics
        top_product=top_product
    )

@app.route("/sales", methods=["GET","POST"])
def sales():

    con = sqlite3.connect("database.db")
    cur = con.cursor()


    if request.method == "POST":

        product_id = request.form["product"]
        qty = int(request.form["qty"])

        cur.execute("SELECT name, price FROM products WHERE id=?", (product_id,))
        product = cur.fetchone()

        name = product[0]
        price = product[1]

        total = price * qty

        item = {
            "product_id": product_id,
            "name": name,
            "price": price,
            "qty": qty,
            "total": total
        }

        cart = session["cart"]
        cart.append(item)
        session["cart"] = cart

    cur.execute("SELECT id, name, price FROM products")
    products = cur.fetchall()

    return render_template(
    "sales.html",
    products=products,
    cart=session.get("cart", [])
)


@app.route("/purchases", methods=["GET","POST"])
def purchases():
    con = get_db()
    cur = con.cursor()

    if request.method == "POST":
        supplier = request.form["supplier"]
        product = request.form["product"]
        qty = int(request.form["qty"])
        price=float(request.form["price"])
        total=qty*price

        # Insert purchase
        cur.execute(
    "insert into purchases (supplier_id, product_id, qty, price, total, date) values (?,?,?,?,?,date('now'))",
    (supplier, product, qty, price, total)
)
        # Update product quantity
        cur.execute(
            "update products set qty = qty + ? where id = ?",
            (qty, product)
        )

        con.commit()
        return redirect("/purchase_bill")

    # Fetch suppliers
    cur.execute("select * from suppliers")
    suppliers = cur.fetchall()

    # Fetch products
    cur.execute("select * from products")
    products = cur.fetchall()

    # Purchase history
    cur.execute("""
    select s.name,
           p.name,
           pu.qty,
           pu.date,
           pu.id
    from purchases pu
    join suppliers s on pu.supplier_id = s.id
    join products p on pu.product_id = p.id
""")
    purchases = cur.fetchall()

    return render_template(
        "purchases.html",
        suppliers=suppliers,
        products=products,
        purchases=purchases
    )

@app.route("/delete_purchase/<int:id>")
def delete_purchase(id):

    con = get_db()
    cur = con.cursor()

    # Get purchase details first
    cur.execute("""
        SELECT product_id, qty
        FROM purchases
        WHERE id=?
    """, (id,))

    purchase = cur.fetchone()

    product_id = purchase[0]
    qty = purchase[1]

    # Reduce stock
    cur.execute("""
        UPDATE products
        SET qty = qty - ?
        WHERE id = ?
    """, (qty, product_id))

    # Delete purchase
    cur.execute("""
        DELETE FROM purchases
        WHERE id=?
    """, (id,))

    con.commit()
    con.close()

    return redirect("/purchases")


@app.route("/edit_purchase/<int:id>", methods=["GET", "POST"])
def edit_purchase(id):

    con = get_db()
    cur = con.cursor()

    # UPDATE PURCHASE
    if request.method == "POST":

        new_qty = int(request.form["qty"])
        new_price = float(request.form["price"])

        # Old purchase details
        cur.execute("""
            SELECT product_id, qty
            FROM purchases
            WHERE id=?
        """, (id,))

        old_purchase = cur.fetchone()

        product_id = old_purchase[0]
        old_qty = old_purchase[1]

        # Calculate stock difference
        difference = new_qty - old_qty

        # Update stock correctly
        cur.execute("""
            UPDATE products
            SET qty = qty + ?
            WHERE id=?
        """, (difference, product_id))

        # New total
        total = new_qty * new_price

        # Update purchase
        cur.execute("""
            UPDATE purchases
            SET qty=?, price=?, total=?
            WHERE id=?
        """, (new_qty, new_price, total, id))

        con.commit()

        return redirect("/purchases")

    # FETCH PURCHASE
    cur.execute("""
        SELECT *
        FROM purchases
        WHERE id=?
    """, (id,))

    purchase = cur.fetchone()

    con.close()

    return render_template(
        "edit_purchase.html",
        purchase=purchase
    )


@app.route("/purchase_bill")
def purchase_bill():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("""
    select s.name,p.name,pu.qty,pu.price,pu.total,pu.date from purchases pu
    join suppliers s on pu.supplier_id=s.id
    join products p on pu.product_id=p.id
    order by pu.id desc
    limit 1
     """)
    bill=cur.fetchone()
    return render_template("purchase_bill.html",bill=bill)


@app.route("/generate_bill")
def generate_bill():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cart=session.get("cart",[])
    grand_total=0

    for item in cart:
        product_id=item["product_id"]
        qty=item["qty"]
        price=item["price"]
        total=item["total"]

        grand_total+=total
        # saving sale in database
        cur.execute("insert into sales (product_id,qty,price,total,date) values(?,?,?,?,date('now'))", (product_id,qty,price,total))

        #To reduce Stock s
        cur.execute("update products set qty=qty-? where id=?",(qty,product_id))
        con.commit()
        session["cart"]=[]
    return render_template("bill.html",cart=cart,total=grand_total)

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        username= request.form.get("username")
        password = request.form.get("password")

        con = sqlite3.connect("database.db")
        cur = con.cursor()

        cur.execute("insert into users(username,password) values(?,?)",(username,password))
        con.commit()
        return redirect("/")

    return render_template("register.html")    


@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        print("USERNAME:", username)
        print("PASSWORD:", password)

        con = sqlite3.connect("database.db")
        cur = con.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cur.fetchone()

        print("USER:", user)

        con.close()

        if user:

            # Store logged-in user
            session["user"] = username

            # Create empty cart if not exists
            if "cart" not in session:
                session["cart"] = []

            return redirect("/dashboard")

        return render_template(
            "login.html",
            error="Invalid Username or Password"
        )

    return render_template("login.html")


    
@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)