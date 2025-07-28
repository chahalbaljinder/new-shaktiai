const { Pool } = require('pg')
const bcrypt = require('bcryptjs')

const pool = new Pool({
  host: 'localhost',
  database: 'shakti_ai_db',
  user: 'postgres',
  password: 'Anjo@024',
  port: 5432,
})

async function initDatabase() {
  try {
    console.log('🛠️  Initializing SHAKTI-AI database...')
    
    // Test database connection first
    const client = await pool.connect()
    console.log('✅ Database connection successful!')
    client.release()
    
    // Create users table
    await pool.query(`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `)
    console.log('✅ Users table created/verified')
    
    // Create index on email for faster lookups
    await pool.query(`
      CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)
    `)
    console.log('✅ Email index created/verified')
    
    // Hash the test password properly
    const testPassword = await bcrypt.hash('test123', 12)
    
    // Insert a test user
    const result = await pool.query(`
      INSERT INTO users (name, email, password) 
      VALUES ($1, $2, $3)
      ON CONFLICT (email) DO NOTHING
      RETURNING id
    `, ['Test User', 'test@example.com', testPassword])
    
    if (result.rows.length > 0) {
      console.log('✅ Test user created')
    } else {
      console.log('ℹ️  Test user already exists')
    }
    
    console.log('')
    console.log('🎉 Database initialization complete!')
    console.log('📧 Test credentials:')
    console.log('   Email: test@example.com')
    console.log('   Password: test123')
    console.log('')
    
  } catch (error) {
    console.error('❌ Database initialization failed:')
    console.error(error.message)
    
    if (error.message.includes('ECONNREFUSED')) {
      console.log('')
      console.log('💡 Troubleshooting:')
      console.log('1. Make sure PostgreSQL is running')
      console.log('2. Check your database credentials in .env.local')
      console.log('3. Verify the database "shakti_ai_db" exists')
    }
    
    process.exit(1)
  } finally {
    await pool.end()
  }
}

// Run the initialization
initDatabase()
