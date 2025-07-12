export default function Home() {
  return (
    <html lang="es">
      <head>
        <title>Asgard Store</title>
        <meta name="description" content="Tienda de ropa Asgard Store" />
      </head>
      <body style={{ 
        margin: 0, 
        padding: 0, 
        fontFamily: 'Arial, sans-serif',
        backgroundColor: '#1a1a1a',
        color: 'white'
      }}>
        <div style={{ 
          minHeight: '100vh',
          padding: '20px'
        }}>
          {/* Header */}
          <header style={{ 
            textAlign: 'center', 
            marginBottom: '40px',
            padding: '20px',
            backgroundColor: '#2a2a2a',
            borderRadius: '10px'
          }}>
            <h1 style={{ 
              fontSize: '3rem', 
              margin: '0 0 10px 0',
              color: '#00ff88'
            }}>
              ASGARD STORE
            </h1>
            <p style={{ 
              fontSize: '1.2rem', 
              margin: 0,
              color: '#cccccc'
            }}>
              Bienvenido a nuestra tienda de ropa
            </p>
          </header>

          {/* Main Content */}
          <main>
            {/* Products Section */}
            <section style={{ marginBottom: '40px' }}>
              <h2 style={{ 
                textAlign: 'center', 
                fontSize: '2rem',
                marginBottom: '30px',
                color: '#00ff88'
              }}>
                Productos Destacados
              </h2>
              
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                gap: '20px',
                maxWidth: '1200px',
                margin: '0 auto'
              }}>
                {[
                  { name: "Camiseta Cyberpunk", price: "$29.99", color: "#ff6b6b" },
                  { name: "Hoodie Retro", price: "$39.99", color: "#4ecdc4" },
                  { name: "Pantalones Tech", price: "$49.99", color: "#45b7d1" },
                  { name: "Zapatos Futuristas", price: "$59.99", color: "#96ceb4" }
                ].map((product, index) => (
                  <div key={index} style={{
                    backgroundColor: '#2a2a2a',
                    padding: '20px',
                    borderRadius: '10px',
                    border: `2px solid ${product.color}`,
                    textAlign: 'center'
                  }}>
                    <h3 style={{ 
                      fontSize: '1.3rem',
                      margin: '0 0 10px 0',
                      color: product.color
                    }}>
                      {product.name}
                    </h3>
                    <p style={{ 
                      fontSize: '1.5rem',
                      fontWeight: 'bold',
                      margin: 0,
                      color: '#00ff88'
                    }}>
                      {product.price}
                    </p>
                  </div>
                ))}
              </div>
            </section>

            {/* Analytics Section */}
            <section style={{ 
              textAlign: 'center',
              backgroundColor: '#2a2a2a',
              padding: '30px',
              borderRadius: '10px'
            }}>
              <h2 style={{ 
                fontSize: '2rem',
                marginBottom: '20px',
                color: '#00ff88'
              }}>
                Análisis Predictivo
              </h2>
              
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '20px',
                maxWidth: '800px',
                margin: '0 auto'
              }}>
                <div style={{
                  backgroundColor: '#ff6b6b',
                  padding: '20px',
                  borderRadius: '8px'
                }}>
                  <h3 style={{ margin: '0 0 10px 0' }}>Tendencia 1</h3>
                  <p style={{ fontSize: '1.2rem', margin: 0 }}>+15% crecimiento</p>
                </div>
                
                <div style={{
                  backgroundColor: '#4ecdc4',
                  padding: '20px',
                  borderRadius: '8px'
                }}>
                  <h3 style={{ margin: '0 0 10px 0' }}>Tendencia 2</h3>
                  <p style={{ fontSize: '1.2rem', margin: 0 }}>+22% crecimiento</p>
                </div>
                
                <div style={{
                  backgroundColor: '#45b7d1',
                  padding: '20px',
                  borderRadius: '8px'
                }}>
                  <h3 style={{ margin: '0 0 10px 0' }}>Tendencia 3</h3>
                  <p style={{ fontSize: '1.2rem', margin: 0 }}>+8% crecimiento</p>
                </div>
              </div>
            </section>
          </main>

          {/* Footer */}
          <footer style={{ 
            textAlign: 'center',
            marginTop: '40px',
            padding: '20px',
            backgroundColor: '#2a2a2a',
            borderRadius: '10px'
          }}>
            <p style={{ 
              margin: 0,
              color: '#cccccc'
            }}>
              © 2024 Asgard Store. Todos los derechos reservados.
            </p>
          </footer>
        </div>
      </body>
    </html>
  )
}
