"use client";

import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Search,
  ShoppingCart,
  TrendingUp,
  Users,
  Package,
  Star,
} from "lucide-react";
import { useInView } from "@/hooks/useInView";
import {
  AnimatedDiv,
  StaggerContainer,
  useScrollAnimation,
} from "./animations";

export function AsgardDashboard() {
  const { ref: heroRef, isInView: heroInView } = useInView({
    triggerOnce: true,
  });
  const scrollAnimation = useScrollAnimation();

  const stats = [
    {
      title: "Productos Vendidos",
      value: "1,234",
      change: "+12%",
      icon: Package,
      color: "text-blue-500",
    },
    {
      title: "Ingresos",
      value: "$45,678",
      change: "+8%",
      icon: TrendingUp,
      color: "text-green-500",
    },
    {
      title: "Clientes",
      value: "567",
      change: "+15%",
      icon: Users,
      color: "text-purple-500",
    },
    {
      title: "Valoración",
      value: "4.8",
      change: "+0.2",
      icon: Star,
      color: "text-yellow-500",
    },
  ];

  const recentProducts = [
    {
      id: 1,
      name: "Circuit Board Tee",
      category: "Camisetas",
      price: "$29.99",
      status: "En Stock",
      sales: 45,
    },
    {
      id: 2,
      name: "Glitch Art Hoodie",
      category: "Sudaderas",
      price: "$49.99",
      status: "Agotado",
      sales: 23,
    },
    {
      id: 3,
      name: "Neon Grid Leggings",
      category: "Pantalones",
      price: "$39.99",
      status: "En Stock",
      sales: 67,
    },
  ];

  return (
    <div className="min-h-screen bg-background p-6">
      {/* Header */}
      <AnimatedDiv variant="fadeInDown" className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-foreground">
              Dashboard AsgardStore
            </h1>
            <p className="text-muted-foreground">
              Bienvenido de vuelta, administrador
            </p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
              <Input placeholder="Buscar productos..." className="pl-10 w-64" />
            </div>
            <Button>
              <ShoppingCart className="w-4 h-4 mr-2" />
              Ver Carrito
            </Button>
          </div>
        </div>
      </AnimatedDiv>

      {/* Stats Grid */}
      <StaggerContainer className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat, index) => (
          <AnimatedDiv key={stat.title} delay={index * 0.1}>
            <Card className="hover:shadow-lg transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">
                      {stat.title}
                    </p>
                    <p className="text-2xl font-bold text-foreground">
                      {stat.value}
                    </p>
                    <Badge variant="secondary" className="mt-2">
                      {stat.change}
                    </Badge>
                  </div>
                  <div className={`p-3 rounded-full bg-muted ${stat.color}`}>
                    <stat.icon className="w-6 h-6" />
                  </div>
                </div>
              </CardContent>
            </Card>
          </AnimatedDiv>
        ))}
      </StaggerContainer>

      {/* Recent Products */}
      <AnimatedDiv {...scrollAnimation} className="mb-8">
        <Card>
          <CardHeader>
            <CardTitle>Productos Recientes</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentProducts.map((product) => (
                <motion.div
                  key={product.id}
                  className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/50 transition-colors"
                  whileHover={{ x: 5 }}
                  transition={{ duration: 0.2 }}
                >
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-gradient-to-br from-primary to-primary/70 rounded-lg flex items-center justify-center">
                      <Package className="w-6 h-6 text-primary-foreground" />
                    </div>
                    <div>
                      <h3 className="font-medium text-foreground">
                        {product.name}
                      </h3>
                      <p className="text-sm text-muted-foreground">
                        {product.category}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-4">
                    <div className="text-right">
                      <p className="font-medium text-foreground">
                        {product.price}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        {product.sales} ventas
                      </p>
                    </div>
                    <Badge
                      variant={
                        product.status === "En Stock"
                          ? "default"
                          : "destructive"
                      }
                    >
                      {product.status}
                    </Badge>
                  </div>
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>
      </AnimatedDiv>

      {/* Quick Actions */}
      <AnimatedDiv
        {...scrollAnimation}
        className="grid grid-cols-1 md:grid-cols-3 gap-6"
      >
        <Card className="hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
          <CardContent className="p-6">
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <Package className="w-6 h-6 text-white" />
              </div>
              <h3 className="font-semibold text-foreground mb-2">
                Agregar Producto
              </h3>
              <p className="text-sm text-muted-foreground mb-4">
                Añade nuevos productos a tu catálogo
              </p>
              <Button className="w-full">Crear Producto</Button>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
          <CardContent className="p-6">
            <div className="text-center">
              <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="w-6 h-6 text-white" />
              </div>
              <h3 className="font-semibold text-foreground mb-2">
                Ver Reportes
              </h3>
              <p className="text-sm text-muted-foreground mb-4">
                Analiza el rendimiento de tu tienda
              </p>
              <Button variant="outline" className="w-full">
                Ver Reportes
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
          <CardContent className="p-6">
            <div className="text-center">
              <div className="w-12 h-12 bg-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="w-6 h-6 text-white" />
              </div>
              <h3 className="font-semibold text-foreground mb-2">
                Gestionar Clientes
              </h3>
              <p className="text-sm text-muted-foreground mb-4">
                Administra tu base de clientes
              </p>
              <Button variant="outline" className="w-full">
                Ver Clientes
              </Button>
            </div>
          </CardContent>
        </Card>
      </AnimatedDiv>
    </div>
  );
}
