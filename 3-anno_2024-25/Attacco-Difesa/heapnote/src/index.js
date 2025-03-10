const sqlite3 = require('sqlite3');
const express = require('express');
const bodyParser = require('body-parser');
const session = require('express-session');
const fs = require('fs');
const crypto = require('crypto');
const path = require('path');

const port = 3000;

// Data directory.
const dir = "./data";

// Ensure the data directory is present.
if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
}

const db = new sqlite3.Database(path.join(dir, "db.sqlite"));

var app = express();

app.set('view engine', 'ejs');

app.use(bodyParser.urlencoded({ extended: true }));

// Execute migrations.
fs.readdirSync("migrations").forEach(file => {
    db.run(fs.readFileSync(path.join("migrations", file), { encoding: "utf-8" }));
});

app.use(session({
    secret: 'edopuzza',
    resave: false,
    saveUninitialized: true
}));

app.post("/register", (req, res) => {
    const username = req.body.username;
    const password = req.body.password;

    if ((username === undefined) || (password === undefined)) {
        res.status(400).send("Invalid username or password.");
        return;
    }

    if (fs.existsSync(path.join(dir, "username"))) {
        res.status(400).send("The user already exists.");
        return;
    }

    db.run("INSERT INTO user(name, hash, created_at) VALUES($name, $hash, datetime('now'));", {
        $name: username,
        $hash: crypto.pbkdf2Sync(password, "no-salt", 10, 64, `sha512`).toString(`hex`),
    }, (out) => {
        if (out === null) {
            req.session.name = username;
            fs.mkdirSync(path.join(dir, username), { recursive: true });

            res.redirect("/");
            return;
        }

        res.status(500).send("There was an error talking to the database.");
        console.error(out);
    })
});

app.get("/newusers", (req, res) => {
    db.all("SELECT * FROM user WHERE created_at > datetime('now', '-15 minutes')", {}, (err, rows) => {
        if (err !== null) {
            res.status(500).send("There was an error retrieving the latest users.");
            return;
        }

        res.render("newusers", { newusers: rows })
        res.status(200);
    })
})

app.post("/login", (req, res) => {
    const username = req.body.username;
    const password = req.body.password;

    if ((username === undefined) || (password === undefined)) {
        res.status(400).send("Invalid username or password.");
        return;
    }

    if (!fs.existsSync(path.join(dir, username))) {
        res.status(400).send("The user doesn't exists.");
        return;
    }

    db.all("SELECT name, hash FROM user WHERE name = $name AND hash = $hash;", {
        $name: username,
        $hash: crypto.pbkdf2Sync(password, "no-salt", 10, 64, `sha512`).toString(`hex`),
    }, (err, rows) => {
        if (err !== null) {
            res.status(500).send("There was an error talking to the database.");
            console.error(err);
            return;
        } else if (rows.length == 0) {
            res.status(403).send("Unauthorized.");
            return;
        }

        req.session.name = username;
        res.redirect("/");
        return;
    })
});

app.get("/login", (req, res) => {
    res.render("login");
});

app.get("/register", (req, res) => {
    res.render("register");
});

const router = express.Router();
router.use((req, res, next) => {
    if (req.session.name === undefined) {
        res.redirect("/login");
        return;
    }

    next();
})

router.get("/", (req, res) => {
    var files = new Array();

    fs.readdirSync(path.join(dir, req.session.name)).forEach(file => {
        files.push({
            url: "/note?id=" + file,
            content: fs.readFileSync(path.join(dir, req.session.name, file), { encoding: "utf-8" }),
        });
    });

    res.render("notes", { files: files });
})

router.post("/note/new", (req, res) => {
    const c = req.body.content;
    var i = 0;

    // Ugly as fuck, but it is what it is :)
    while (fs.existsSync(path.join(dir, req.session.name, i.toString()))) {
        i++;
    }

    fs.writeFileSync(path.join(dir, req.session.name, i.toString()), c);
    res.redirect("/note?id=" + i.toString());
})

router.get("/note/new", (req, res) => {
    res.render("addnote");
})

router.get("/note", (req, res) => {
    let id = req.query.id;
    if (id === undefined) {
        res.status(400).send("You have to provide a note id!");
        return;
    }

    file = fs.readFileSync(path.join(dir, req.session.name, id), { encoding: "utf-8" })
    res.render("note", { file: file, id: id });
})

app.use('/', router);

app.listen(port, () => {
    console.log(`heapnote listening on port ${port}`)
})