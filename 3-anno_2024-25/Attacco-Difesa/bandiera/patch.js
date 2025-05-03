var express = require('express');
var session = require('express-session');
var bodyParser = require('body-parser');
var mysql = require('mysql2');
const helmet = require('helmet'); // Add security headers
const rateLimit = require('express-rate-limit'); // Add rate limiting

// Create connection pool with improved error handling
const pool = mysql.createPool({
  host: process.env.MYSQL_HOST,
  user: process.env.MYSQL_USER,
  password: process.env.MYSQL_PASSWORD,
  database: process.env.MYSQL_DB,
  connectionLimit: 5,
});

const port = process.env.PORT || 3000;
var app = express();

// Enhance security with helmet
app.use(helmet());

// Set up rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
});
app.use(limiter);

// Use session with secure settings
app.use(session({
  secret: process.env.SESSION_SECRET || 'need-to-change-this',
  resave: false,
  saveUninitialized: true,
  cookie: { 
    secure: process.env.NODE_ENV === 'production', // Use secure cookies in production
    httpOnly: true, // Prevent client-side JS from reading the cookie
    sameSite: 'strict' // Prevent CSRF attacks
  }
}));

// Parse JSON bodies
app.use(bodyParser.json());

// Create table if not exists
pool.query(`CREATE TABLE IF NOT EXISTS bandiere(
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  testo TEXT NOT NULL
);`, function (error, results, fields) {
  if (error) {
    console.error('Error creating table:', error.message);
    process.exit(1);
  }
});

// POST endpoint to create a new bandiera
app.post('/bandiera', (req, res) => {
  // Validate content type
  if (!req.is('application/json')) {
    return res.status(415).json({"errore": "Content-Type deve essere application/json"});
  }

  const bandiera = req.body.bandiera;
  
  // Validate input
  if (bandiera === undefined || bandiera === null) {
    return res.status(400).json({"errore": "Il campo 'bandiera' non è stato fornito."});
  }
  
  if (typeof bandiera !== 'string') {
    return res.status(400).json({"errore": "Il campo 'bandiera' deve essere una stringa."});
  }
  
  // Insert into database
  pool.query("INSERT INTO bandiere(testo) value(?)", [bandiera], function(err, results, fields) {
    if (err) {
      console.error('Database error:', err.message);
      return res.status(500).json({"errore": "Errore interno del server."});
    }
    
    res.status(201).json({"id": results.insertId});
  });
});

// GET endpoint to retrieve a bandiera by ID
app.get('/bandiera/:id', (req, res) => {
  const id = req.params.id; // Get ID from URL parameter, not body
  
  // Validate ID
  if (!id) {
    return res.status(400).json({"errore": "Il campo 'id' non è stato fornito."});
  }
  
  // Ensure ID is a number
  const idNum = parseInt(id, 10);
  if (isNaN(idNum) || idNum.toString() !== id) {
    return res.status(400).json({"errore": "L'id deve essere un numero intero."});
  }
  
  // Query database
  pool.query("SELECT testo FROM bandiere WHERE id = ? LIMIT 1", [idNum], function(err, results, fields) {
    if (err) {
      console.error('Database error:', err.message);
      return res.status(500).json({"errore": "Errore interno del server."});
    }
    
    if (results.length === 0) {
      return res.status(404).json({"errore": "Non ho trovato la bandiera corrispondente al tuo id."});
    }
    
    res.status(200).json({"bandiera": results[0].testo});
  });
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({"status": "ok"});
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM signal received: closing HTTP server');
  app.close(() => {
    console.log('HTTP server closed');
    pool.end();
  });
});

// Start server
app.listen(port, () => {
  console.log(`bandiera sta ascoltando sulla porta ${port}`);
});