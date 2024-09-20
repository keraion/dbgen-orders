This is a working progress, but should allow the generation of a sample database to build some data pipelines with.

Tables:
    Customer:
        - ID
        - Name
        - DOB
    Customer_Address:
        - ID
        - Customer ID
        - Address Line 1
        - Address Line 2
        - City
        - State
        - Zip
    Order:
        - ID
        - Customer ID
        - Address ID
        - Order Date
        - Order Paid Amount

Still to do:
    Order Status:
        - ID
        - Order ID
        - Status
        - Status Date
    Order_Line_Item:
        - ID
        - Order ID
        - Stock ID
        - Quantity
        - Paid Amount
    Stock:
        - ID
        - Name
        - Quantity
        - Price
