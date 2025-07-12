"use client";

import * as React from "react";
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
import { useInView } from "../hooks/useInView";
import {
  AnimatedDiv,
  StaggerContainer,
  useScrollAnimation,
} from "./animations";
import { useEffect, useState } from "react";

interface AnimatedDivProps extends React.ComponentProps<typeof motion.div> {
  children: React.ReactNode;
  variant?:
    | "fadeInUp"
    | "fadeInDown"
    | "fadeInLeft"
    | "fadeInRight"
    | "scaleIn";
  delay?: number;
}

interface StaggerContainerProps extends React.ComponentProps<typeof motion.div> {
  children: React.ReactNode;
}

export function AsgardDashboard() {
  const { ref: heroRef, isInView: heroInView } = useInView({
    triggerOnce: true,
  });
  const scrollAnimation = useScrollAnimation();
  const [isMobile, setIsMobile] = useState(false);
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  // Detect mobile and reduced motion preferences
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };

    const checkReducedMotion = () => {
      setPrefersReducedMotion(
        window.matchMedia("(prefers-reduced-motion: reduce)").matches
      );
    };

    checkMobile();
    checkReducedMotion();

    const handleResize = () => checkMobile();
    window.addEventListener("resize", handleResize);

    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    mediaQuery.addEventListener("change", checkReducedMotion);

    return () => {
      window.removeEventListener("resize", handleResize);
      mediaQuery.removeEventListener("change", checkReducedMotion);
    };
  }, []);

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
      name: "Collar Espada Zelda TOTK",
      category: "Accesorios",
      description: "Collar inspirado en la Espada Maestra de Zelda: Tears of the Kingdom. Ideal para fans de la saga.",
      price: "$15.99",
      status: "En Stock",
      sales: 12,
      image: "/productos/collar espada Zelda TOTK.jpg",
    },
    {
      id: 2,
      name: "Billetera R2-D2",
      category: "Accesorios",
      description: "Billetera temática de R2-D2, perfecta para los amantes de Star Wars y la cultura geek.",
      price: "$19.99",
      status: "En Stock",
      sales: 8,
      image: "/productos/billetera R2-D2.jpg",
    },
    {
      id: 3,
      name: "Gorra Venom",
      category: "Gorras",
      description: "Gorra negra con diseño de Venom, cómoda y con mucho estilo para los fans de Marvel.",
      price: "$14.99",
      status: "En Stock",
      sales: 20,
      image: "/productos/gorra venom.jpg",
    },
    {
      id: 4,
      name: "Medias Matrix",
      category: "Ropa",
      description: "Medias con diseño inspirado en Matrix, ideales para quienes buscan un toque geek en su vestimenta.",
      price: "$7.99",
      status: "En Stock",
      sales: 15,
      image: "/productos/medias Matrix.jpg",
    },
    {
      id: 5,
      name: "Suéter Armadura Medieval",
      category: "Ropa",
      description: "Suéter con estampado de armadura medieval, perfecto para destacar en cualquier ocasión.",
      price: "$29.99",
      status: "En Stock",
      sales: 5,
      image: "/productos/sueter armadura medieval.jpeg",
    },
    {
      id: 6,
      name: "Franela Retro 8bits",
      category: "Camisetas",
      description: "Franela con diseño retro de 8 bits, un clásico para los nostálgicos de los videojuegos.",
      price: "$12.99",
      status: "En Stock",
      sales: 18,
      image: "/productos/franela Retro 8bits.jpg",
    },
    {
      id: 7,
      name: "Chaqueta Cyberpunk",
      category: "Chaquetas",
      description: "Chaqueta con estilo cyberpunk, moderna y llamativa para quienes buscan un look futurista.",
      price: "$39.99",
      status: "En Stock",
      sales: 7,
      image: "/productos/chaqueta Cyberpunk.jpg",
    },
  ];

  return (
    <div className="min-h-screen bg-background p-6">
      {/* Header */}
      <AnimatedDiv
        variant="fadeInDown"
        className={`mb-8 ${isMobile ? "mobile-reduce-motion" : ""}`}
      >
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-foreground">
              Dashboard AsgardStore
            </h1>
            <p className="text-muted-foreground">
              Bienvenido de vuelta, administrador
            </p>
          </div>
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
              <Input
                placeholder="Buscar productos..."
                className="pl-10 w-full sm:w-64"
              />
            </div>
            <Button className="w-full sm:w-auto">
              <ShoppingCart className="w-4 h-4 mr-2" />
              Ver Carrito
            </Button>
          </div>
        </div>
      </AnimatedDiv>

      {/* Stats Grid */}
      <StaggerContainer className={"grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-8"}>
        {stats.map((stat, index) => (
          <AnimatedDiv
            key={stat.title}
            delay={prefersReducedMotion ? 0 : index * 0.1}
            className={isMobile ? "mobile-reduce-motion" : ""}
          >
            <Card className="card-hover hover:shadow-lg transition-shadow group">
              <CardContent className="p-4 md:p-6 text-card-paragraph group-hover:text-card-paragraph-hover">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-xs md:text-sm font-medium text-muted-foreground">
                      {stat.title}
                    </p>
                    <p className="text-xl md:text-2xl font-bold text-foreground">
                      {stat.value}
                    </p>
                    <Badge variant="secondary" className="mt-2 text-xs">
                      {stat.change}
                    </Badge>
                  </div>
                  <div
                    className={`p-2 md:p-3 rounded-full bg-muted ${stat.color}`}
                  >
                    <stat.icon className="w-4 h-4 md:w-6 md:h-6" />
                  </div>
                </div>
              </CardContent>
            </Card>
          </AnimatedDiv>
        ))}
      </StaggerContainer>

      {/* Recent Products */}
      <motion.div
        variants={scrollAnimation.variants}
        initial={scrollAnimation.initial}
        whileInView={scrollAnimation.whileInView}
        viewport={scrollAnimation.viewport}
        className="mb-8"
        style={{
          willChange: prefersReducedMotion ? "auto" : "transform, opacity",
          contain: "layout style paint",
        }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Productos Recientes</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentProducts.map((product) => (
                <motion.div
                  key={product.id}
                  className="flex flex-col sm:flex-row sm:items-center sm:justify-between p-4 border rounded-lg hover:bg-muted/50 transition-colors card-hover group"
                  whileHover={prefersReducedMotion ? {} : { x: 5 }}
                  transition={{ duration: prefersReducedMotion ? 0 : 0.2, ease: [0.42, 0, 0.58, 1] }}
                  style={{
                    willChange: prefersReducedMotion ? "auto" : "transform",
                    contain: "layout style paint",
                  }}
                >
                  <div className="flex items-center space-x-4 mb-2 sm:mb-0">
                    <img
                      src={product.image}
                      alt={product.name}
                      className="w-10 h-10 md:w-12 md:h-12 rounded-lg object-cover"
                    />
                    <div>
                      <h3 className="font-medium text-foreground text-sm md:text-base">
                        {product.name}
                      </h3>
                      <p className="text-xs md:text-sm text-muted-foreground">
                        {product.category}
                      </p>
                      <p className="text-xs text-muted-foreground mt-1">
                        {product.description}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center justify-between sm:space-x-4">
                    <div className="text-right">
                      <p className="font-medium text-foreground text-sm md:text-base">
                        {product.price}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {product.sales} ventas
                      </p>
                    </div>
                    <Badge
                      variant={
                        product.status === "En Stock"
                          ? "default"
                          : "destructive"
                      }
                      className="text-xs"
                    >
                      {product.status}
                    </Badge>
                  </div>
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Quick Actions */}
      <motion.div
        variants={scrollAnimation.variants}
        initial={scrollAnimation.initial}
        whileInView={scrollAnimation.whileInView}
        viewport={scrollAnimation.viewport}
        className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6"
        style={{
          willChange: prefersReducedMotion ? "auto" : "transform, opacity",
          contain: "layout style paint",
        }}
      >
        <Card className="card-hover hover:shadow-lg transition-all duration-300 hover:-translate-y-1 group">
          <CardContent className="p-4 md:p-6">
            <div className="text-center">
              <div className="w-10 h-10 md:w-12 md:h-12 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <Package className="w-5 h-5 md:w-6 md:h-6 text-white" />
              </div>
              <h3 className="font-semibold text-foreground mb-2 text-sm md:text-base">
                Agregar Producto
              </h3>
              <p className="text-xs md:text-sm text-muted-foreground mb-4">
                Añade nuevos productos a tu catálogo
              </p>
              <Button className="w-full text-sm bg-asgard-purple hover:bg-asgard-purple-hover text-white hover:shadow-[0_4px_24px_0_rgba(120,71,235,0.5)]">
                Crear Producto
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="card-hover hover:shadow-lg transition-all duration-300 hover:-translate-y-1 group">
          <CardContent className="p-4 md:p-6">
            <div className="text-center">
              <div className="w-10 h-10 md:w-12 md:h-12 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="w-5 h-5 md:w-6 md:h-6 text-white" />
              </div>
              <h3 className="font-semibold text-foreground mb-2 text-sm md:text-base">
                Ver Reportes
              </h3>
              <p className="text-xs md:text-sm text-muted-foreground mb-4">
                Analiza el rendimiento de tu tienda
              </p>
              <Button className="w-full text-sm bg-asgard-purple hover:bg-asgard-purple-hover text-white hover:shadow-[0_4px_24px_0_rgba(120,71,235,0.5)]">
                Ver Reportes
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="card-hover hover:shadow-lg transition-all duration-300 hover:-translate-y-1 group">
          <CardContent className="p-4 md:p-6">
            <div className="text-center">
              <div className="w-10 h-10 md:w-12 md:h-12 bg-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="w-5 h-5 md:w-6 md:h-6 text-white" />
              </div>
              <h3 className="font-semibold text-foreground mb-2 text-sm md:text-base">
                Gestionar Clientes
              </h3>
              <p className="text-xs md:text-sm text-muted-foreground mb-4">
                Administra tu base de clientes
              </p>
              <Button className="w-full text-sm bg-asgard-purple hover:bg-asgard-purple-hover text-white hover:shadow-[0_4px_24px_0_rgba(120,71,235,0.5)]">
                Ver Clientes
              </Button>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
