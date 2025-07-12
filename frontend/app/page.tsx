"use client"

import { Search } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"
import { useEffect, useState } from "react"
import PredictiveTrends from "@/components/PredictiveTrends"

export default function AsgardStore() {
  const [isLoaded, setIsLoaded] = useState(false)

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoaded(true)
    }, 100)

    return () => clearTimeout(timer)
  }, [])

  return (
    <div className="min-h-screen bg-[#171221] text-white">
      {/* Header */}
      <header className="border-b border-[#2e2447] px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-8">
            <div className="flex items-center space-x-2">
              <div
                className="w-6 h-6 bg-white"
                style={{
                  clipPath: "polygon(50% 0%, 0% 100%, 100% 100%)",
                }}
              />
              <span className="text-xl font-bold">
                ASGARD STORE
              </span>
            </div>
            <nav className="hidden md:flex space-x-6">
              {["Novedades", "Hombres", "Mujeres", "Accesorios"].map((item) => (
                <a
                  key={item}
                  href="#"
                  className="text-[#a394c7] hover:text-white"
                >
                  {item}
                </a>
              ))}
            </nav>
          </div>
          <div className="flex items-center space-x-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-[#a394c7] w-4 h-4" />
              <Input
                placeholder="Buscar"
                className="pl-10 bg-[#2e2447] border-[#2e2447] text-white placeholder:text-[#a394c7] w-64"
              />
            </div>
            <Button className="border-[#7847eb] text-[#7847eb] hover:bg-[#7847eb] hover:text-white bg-transparent border">
              Iniciar Sesión
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="px-6 py-16">
        <div className="max-w-7xl mx-auto">
          <div className="relative rounded-2xl overflow-hidden">
            <div className="w-full h-[400px] bg-gradient-to-r from-teal-900 via-teal-700 to-cyan-600 flex items-center justify-center">
              <div className="text-center">
                <h1 className="text-5xl font-bold mb-4">
                  Bienvenido a Asgard Store
                </h1>
                <p className="text-xl text-cyan-200 mb-8">
                  Descubre las últimas tendencias en moda
                </p>
                <Button className="bg-[#7847eb] hover:bg-[#7847eb]/90 text-white px-8 py-3 text-lg">
                  Explorar Colección
                </Button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Products Section */}
      <section className="px-6 py-16">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold mb-8 text-center">Productos Destacados</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              {
                title: "Circuit Board Tee",
                description: "A stylish tee featuring a circuit board design.",
                gradient: "from-green-600 to-green-800",
              },
              {
                title: "Glitch Art Hoodie",
                description: "A comfortable hoodie with a glitch art pattern.",
                gradient: "from-blue-800 to-blue-900",
              },
              {
                title: "Neon Grid Leggings",
                description: "Eye-catching leggings with a neon grid design.",
                gradient: "from-purple-600 to-pink-600",
              },
              {
                title: "Binary Code Scarf",
                description: "A unique scarf with a binary code pattern.",
                gradient: "from-gray-700 to-gray-900",
              },
            ].map((product, index) => (
              <Card key={index} className="bg-[#2e2447] border-[#2e2447] overflow-hidden">
                <CardContent className="p-0">
                  <div className={`h-64 bg-gradient-to-br ${product.gradient} flex items-center justify-center`}>
                    <div className="text-center">
                      <div className="text-4xl mb-2">👕</div>
                    </div>
                  </div>
                  <div className="p-4">
                    <h3 className="font-bold mb-1">{product.title}</h3>
                    <p className="text-[#a394c7] text-sm">{product.description}</p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Predictive Trends Section */}
      <section className="px-6 py-16 bg-[#1a1a2e]">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4">
              Análisis Predictivo de Tendencias
            </h2>
            <p className="text-[#a394c7] text-lg">
              Descubre las tendencias futuras con nuestro modelo de machine learning
            </p>
          </div>
          <PredictiveTrends />
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-[#2e2447] px-6 py-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center text-[#a394c7] text-sm">
            © 2024 Asgard Store. Todos los Derechos Reservados.
          </div>
        </div>
      </footer>
    </div>
  )
}
