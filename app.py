import os
from urllib.parse import unquote
import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from pymongo import MongoClient
from logging import basicConfig, INFO, FileHandler, StreamHandler, getLogger, ERROR
from methods import algorithms

if os.path.exists("log.txt"):
    with open("log.txt", "w"):
        pass

basicConfig(
    format="%(asctime)s: [%(levelname)s: %(filename)s - %(lineno)d] ~ %(message)s",
    handlers=[FileHandler("log.txt", mode="w"), StreamHandler()],
    datefmt="%d-%b-%y %I:%M:%S %p",
    level=INFO,
)

getLogger("pyrogram").setLevel(ERROR)
getLogger("urllib3").setLevel(ERROR)
getLogger("PIL").setLevel(ERROR)

LOGGER = getLogger(__name__)

LOGGER.info("Logger initialized and log file cleared.")

app = FastAPI()

DB_URL = "mongodb+srv://rushidhar:rushidharr@rushiapi.zh3kb.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(DB_URL)
db = client["flipkart"]
collection = db["products"]



class DirectDownloadLinkException(Exception):
    pass


rawhtml_one = """<html>
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Products</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous" />
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background: black;
            color: #fff;
            display: flex;
            justify-content: flex-start;
            align-items: flex-start;
            flex-direction: column;
            margin: 0;
            padding: 0;
            min-height: 100vh; /* Ensure it takes at least the full height of the screen */
        }

        h1 {
            font-family: 'Dancing Script', cursive;
            color: #FFDC00;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
            font-weight: bold;
        }

        .product-card {
            display: flex;
            width: 100%;
            background-color: #333;
            border-radius: 15px;
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.3);
            margin: 15px 0;
            transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
        }

        .product-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 25px rgba(0, 0, 0, 0.4);
        }

        .product-image {
            width: 150px;
            height: 150px;
            background-size: cover;
            background-position: center;
            border-radius: 15px 0 0 15px;
        }

        .product-info {
            padding: 20px;
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .product-name {
            font-size: 1.4em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #f1f1f1;
            word-wrap: break-word;
        }

        .price-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 10px;
        }

        .price {
            font-size: 1.5em;
            color: #FF6F61;
            font-weight: bold;
        }

        .original-price {
            text-decoration: line-through;
            color: #999;
            font-size: 1.1em;
        }

        .discount {
            background-color: #28a745;
            color: white;
            font-size: 1em;
            padding: 5px 10px;
            border-radius: 5px;
        }

        .product-link {
            text-decoration: none;
            background-color: #007bff;
            color: white;
            padding: 12px;
            text-align: center;
            border-radius: 8px;
            font-weight: bold;
            margin-top: 15px;
            transition: background-color 0.3s ease-in-out;
        }

        .product-link:hover {
            background-color: #0056b3;
        }

        .search-container {
            width: 80%;
            text-align: center;
            margin-bottom: 20px;
        }

        .search-bar {
            width: 300px;
            padding: 12px;
            font-size: 1.1em;
            border-radius: 5px;
            border: 1px solid #333;
            background-color: #444;
            color: #fff;
        }

        .footer {
            background-color: #333;
            padding: 10px 0;
            width: 100%;
            text-align: center;
            font-size: 1.1em;
            border-radius: 15px;
            position: relative;
            bottom: 0;
        }

        .footer a {
            color: #FFDC00;
            font-weight: bold;
        }

        .content-wrapper {
            margin-top: 10px; /* Add gap here for the header */
            margin-bottom: 10px;
            width: 100%;
            flex-grow: 1; /* Allow content to grow and take the remaining space */
        }

        .header {
            background-color: #333;
            padding: 10px 0;
            width: 100%;
            text-align: center;
            font-size: 1.1em;
            border-radius: 15px;
            position: relative;
            z-index: 1;
        }
    </style>
  </head>
  <body>
    <div class="container-fluid">
        <div class="row">
            <div class="header">
                <h1 class="text-center">AURORA UNIVERSITY</h1>
            </div>

            <div class="content-wrapper">
"""

rawhtml_two = """            </div>

            <div class="footer">
                <p>Made with 💛 by <a href="https://telegram.me/Rushidhar1999" target="_blank">𝚁𝚞𝚜𝚑𝚒𝚍𝚊𝚛</a></p>
            </div>
        </div>
    </div>
  </body>
</html>
"""
    

@app.get("/search")
async def product_info(request: Request):
    query_params = str(request.url.query).split("q=")[1]
    response_data, visualization = await algorithms(unquote(query_params))
    return HTMLResponse(content=visualization)


@app.get("/")
async def home():
    response_data = {"server": "<h1>Site Running</h1>"}
    return JSONResponse(content=response_data)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
