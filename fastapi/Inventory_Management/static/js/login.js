console.log("login js connected");

const bottom_text = [
    "The Northwind database is a classic, foundational sample database originally created by Microsoft.",
    "It features sales data for a fictional company 'Northwind Traders' that imports and exports specialty foods.",
    "It is widely used to teach RDBMS concepts, SQL queries, and ERP system structures.",
    "The Northwind database has since been ported to a variety of non-Microsoft databases, including PostgreSQL.",
    "The Northwind sample database includes 14 tables and the table relationships are showcased in the following entity relationship diagram."


];

const moving_text_div = document.getElementById("moving_text");

const updateText = () => {
    moving_text_div.classList.add("text-fade");

    setTimeout(() => {

        const randomIndex = Math.floor(Math.random() * bottom_text.length);
        moving_text_div.innerText = bottom_text[randomIndex];

        moving_text_div.classList.remove("text-fade");
    }, 2000);
};

setInterval(updateText, 5000);