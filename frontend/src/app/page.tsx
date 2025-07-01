"use client";

import { Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { useEffect, useState, useMemo } from "react";

export default function AsgardStore() {
  const [isLoaded, setIsLoaded] = useState(false);
  const [visibleCards, setVisibleCards] = useState<number[]>([]);
  const [isMobile, setIsMobile] = useState(false);
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);
  const [isIntersecting, setIsIntersecting] = useState<Record<string, boolean>>(
    {}
  );

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

  // Optimized loading sequence
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoaded(true);
    }, 100);

    // Staggered card animation with reduced delays on mobile
    const cardTimer = setTimeout(
      () => {
        const delay = isMobile ? 50 : 200;
        setVisibleCards([0]);
        setTimeout(() => setVisibleCards([0, 1]), delay);
        setTimeout(() => setVisibleCards([0, 1, 2]), delay * 2);
      },
      isMobile ? 200 : 500
    );

    return () => {
      clearTimeout(timer);
      clearTimeout(cardTimer);
    };
  }, [isMobile]);

  // Intersection Observer for performance
  useEffect(() => {
    if (typeof window === "undefined") return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          setIsIntersecting((prev) => ({
            ...prev,
            [entry.target.id]: entry.isIntersecting,
          }));
        });
      },
      {
        threshold: 0.1,
        rootMargin: "50px",
      }
    );

    const sections = document.querySelectorAll("[data-animate]");
    sections.forEach((section) => observer.observe(section));

    return () => observer.disconnect();
  }, []);

  // Memoized animation classes
  const animationClasses = useMemo(
    () => ({
      header: prefersReducedMotion
        ? "opacity-100"
        : `transition-all duration-${isMobile ? "500" : "1000"} ${
            isLoaded
              ? "translate-y-0 opacity-100"
              : "-translate-y-full opacity-0"
          }`,

      hero: prefersReducedMotion
        ? "opacity-100"
        : `transition-all duration-${isMobile ? "500" : "1000"} ${
            isLoaded ? "scale-100 opacity-100" : "scale-95 opacity-0"
          }`,

      card: (index: number, isVisible: boolean) =>
        prefersReducedMotion
          ? "opacity-100"
          : `transition-all duration-${isMobile ? "300" : "500"} ${
              isVisible
                ? "translate-y-0 opacity-100"
                : "translate-y-8 opacity-0"
            }`,

      hover: prefersReducedMotion
        ? ""
        : isMobile
        ? "active:scale-95"
        : "hover:scale-105 hover:shadow-xl",
    }),
    [prefersReducedMotion, isMobile, isLoaded]
  );

  // Optimized particle count for mobile
  const particleCount = useMemo(() => {
    if (prefersReducedMotion) return 0;
    return isMobile ? 5 : 15;
  }, [isMobile, prefersReducedMotion]);

  // Generate particle styles on client (updated for new structure)
  const [particleStyles, setParticleStyles] = useState<any[]>([]);
  useEffect(() => {
    if (typeof window === "undefined" || prefersReducedMotion) return;
    const generatedParticleStyles = [...Array(particleCount)].map(() => ({
      left: `${Math.random() * 100}%`,
      top: `${Math.random() * 100}%`,
      animation: `ping ${2 + Math.random() * 2}s infinite ${
        Math.random() * 3
      }s`,
      willChange: "transform, opacity",
    }));
    setParticleStyles(generatedParticleStyles);
  }, [particleCount, prefersReducedMotion]); // Re-generate if count changes or motion preference changes

  return (
    <div className="min-h-screen bg-asgard-dark text-white overflow-x-hidden">
      {/* Header - Optimized */}
      <header
        className={`border-b border-asgard-purple px-6 py-4 ${animationClasses.header}`}
      >
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-8">
            <div className="flex items-center space-x-2 group">
              <div
                className={`w-6 h-6 bg-white ${
                  prefersReducedMotion
                    ? ""
                    : "transition-transform duration-300 group-hover:rotate-180"
                }`}
                style={{
                  clipPath: "polygon(50% 0%, 0% 100%, 100% 100%)",
                  willChange: prefersReducedMotion ? "auto" : "transform",
                }}
              />
              <span
                className={`text-xl font-bold ${
                  prefersReducedMotion
                    ? ""
                    : "transition-colors duration-300 group-hover:text-asgard-accent"
                }`}
              >
                ASGARD STORE
              </span>
            </div>
            <nav className="hidden md:flex space-x-6">
              {["Novedades", "Hombres", "Mujeres", "Accesorios"].map(
                (item, index) => (
                  <a
                    key={item}
                    href="#"
                    className={`text-asgard-light-purple hover:text-white relative group ${
                      prefersReducedMotion
                        ? ""
                        : `transition-all duration-300 ${
                            isLoaded
                              ? "translate-y-0 opacity-100"
                              : "translate-y-4 opacity-0"
                          }`
                    }`}
                    style={{
                      transitionDelay: prefersReducedMotion
                        ? "0ms"
                        : `${index * 100 + 200}ms`,
                      willChange: prefersReducedMotion
                        ? "auto"
                        : "transform, opacity",
                    }}
                  >
                    {item}
                    {!prefersReducedMotion && (
                      <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-asgard-accent transition-all duration-300 group-hover:w-full"></span>
                    )}
                  </a>
                )
              )}
            </nav>
          </div>
          <div
            className={`flex items-center space-x-4 ${animationClasses.header}`}
          >
            <div className="relative group">
              <Search
                className={`absolute left-3 top-1/2 transform -translate-y-1/2 text-asgard-light-purple w-4 h-4 ${
                  prefersReducedMotion
                    ? ""
                    : "transition-colors duration-300 group-focus-within:text-asgard-accent"
                }`}
              />
              <Input
                placeholder="Buscar"
                className={`pl-10 bg-asgard-purple border-asgard-purple text-white placeholder:text-card-paragraph focus:border-asgard-purple focus:ring-asgard-purple/20 ${
                  prefersReducedMotion
                    ? ""
                    : "transition-all duration-300 focus:border-asgard-accent focus:ring-2 focus:ring-asgard-accent/20"
                }`}
              />
            </div>
            <Button
              className={`border-asgard-purple text-asgard-purple bg-transparent hover:bg-asgard-purple hover:text-white ${
                prefersReducedMotion
                  ? ""
                  : isMobile
                  ? "active:scale-95 transition-transform duration-150"
                  : "transition-all duration-300 hover:scale-105"
              }`}
              style={{
                willChange: prefersReducedMotion ? "auto" : "transform",
              }}
            >
              Iniciar Sesión
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section - Performance Optimized */}
      <section className="relative px-6 py-16" data-animate id="hero">
        <div className="max-w-7xl mx-auto">
          <div
            className={`relative rounded-2xl overflow-hidden ${animationClasses.hero}`}
          >
            <div
              className="w-full h-[400px] bg-gradient-to-r from-teal-900 via-teal-700 to-cyan-600 flex items-center justify-center relative overflow-hidden"
              style={{ contain: "layout style paint" }}
            >
              {/* Optimized buildings - Reduced on mobile */}
              {!prefersReducedMotion && (
                <div className="absolute inset-0 opacity-30">
                  {(isMobile
                    ? [
                        {
                          left: "33%",
                          width: "3rem",
                          height: "12rem",
                          skew: "-skew-y-1",
                        },
                        {
                          left: "50%",
                          width: "4rem",
                          height: "16rem",
                          skew: "skew-y-1",
                        },
                        {
                          right: "33%",
                          width: "2.5rem",
                          height: "10rem",
                          skew: "-skew-y-2",
                        },
                      ]
                    : [
                        {
                          left: "25%",
                          width: "2rem",
                          height: "8rem",
                          skew: "skew-y-2",
                        },
                        {
                          left: "33%",
                          width: "3rem",
                          height: "12rem",
                          skew: "-skew-y-1",
                        },
                        {
                          left: "50%",
                          width: "4rem",
                          height: "16rem",
                          skew: "skew-y-1",
                        },
                        {
                          right: "33%",
                          width: "2.5rem",
                          height: "10rem",
                          skew: "-skew-y-2",
                        },
                        {
                          right: "25%",
                          width: "3.5rem",
                          height: "14rem",
                          skew: "skew-y-1",
                        },
                      ]
                  ).map((building, index) => (
                    <div
                      key={index}
                      className={`absolute bottom-0 bg-gradient-to-t from-cyan-400 to-teal-300 transform ${building.skew}`}
                      style={{
                        left: building.left,
                        right: building.right,
                        width: building.width,
                        height: building.height,
                        willChange: "auto",
                        animation: isMobile
                          ? "none"
                          : `pulse 3s infinite ${index * 0.2}s`,
                      }}
                    />
                  ))}
                </div>
              )}

              {/* Reduced particles for mobile */}
              {!prefersReducedMotion && isIntersecting.hero && (
                <div className="absolute inset-0">
                  {particleStyles.map((style, i) => (
                    <div
                      key={i}
                      className="absolute w-1 h-1 bg-cyan-300 rounded-full"
                      style={style}
                    />
                  ))}
                </div>
              )}

              <div className="absolute inset-0 bg-black/40 flex items-center justify-center">
                <div className={`text-center z-10 ${animationClasses.hero}`}>
                  <h1
                    className={`text-5xl font-bold mb-4 ${
                      prefersReducedMotion ? "" : "animate-pulse"
                    }`}
                  >
                    <span
                      className={`inline-block ${
                        prefersReducedMotion
                          ? ""
                          : "hover:scale-110 transition-transform duration-300"
                      }`}
                    >
                      Sube
                    </span>{" "}
                    <span
                      className={`inline-block ${
                        prefersReducedMotion
                          ? ""
                          : "hover:scale-110 transition-transform duration-300"
                      }`}
                    >
                      de
                    </span>{" "}
                    <span
                      className={`inline-block text-asgard-accent ${
                        prefersReducedMotion
                          ? ""
                          : "hover:scale-110 transition-transform duration-300"
                      }`}
                    >
                      Nivel
                    </span>{" "}
                    <span
                      className={`inline-block ${
                        prefersReducedMotion
                          ? ""
                          : "hover:scale-110 transition-transform duration-300"
                      }`}
                    >
                      tu
                    </span>{" "}
                    <span
                      className={`inline-block text-cyan-400 ${
                        prefersReducedMotion
                          ? ""
                          : "hover:scale-110 transition-transform duration-300"
                      }`}
                    >
                      Estilo!
                    </span>
                  </h1>
                  <p
                    className={`text-xl text-asgard-light mb-8 ${animationClasses.hero}`}
                  >
                    Armate y expresa tu estilo con ropa inspirada en la cultura
                    Geek
                  </p>
                  <Button
                    className={`bg-asgard-purple hover:bg-asgard-purple-hover text-white hover:shadow-[0_4px_24px_0_rgba(120,71,235,0.5)] px-8 py-3 text-lg relative overflow-hidden group ${
                      prefersReducedMotion
                        ? ""
                        : isMobile
                        ? "active:scale-95 transition-transform duration-150"
                        : "transition-all duration-300 hover:scale-110 hover:shadow-xl hover:shadow-asgard-accent/50"
                    }`}
                    style={{
                      willChange: prefersReducedMotion ? "auto" : "transform",
                    }}
                  >
                    <span className="relative z-10">
                      Comprar
                      {!prefersReducedMotion && (
                        <span className="absolute inset-0 bg-white/20 rounded transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left"></span>
                      )}
                    </span>
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Popular Collections - Optimized */}
      <section className="px-6 py-16" data-animate id="collections">
        <div className="max-w-7xl mx-auto">
          <h2 className={`text-3xl font-bold mb-8 ${animationClasses.hero}`}>
            Colecciones Populares
          </h2>
          <div className="grid md:grid-cols-3 gap-6">
            {[
              {
                title: "Colección Cyberpunk",
                description:
                  "Abraza el futuro con nuestra Colección Cyberpunk. Diseños atrevidos para los amantes de la tecnología.",
                image: "/productos/chaqueta Cyberpunk.jpg",
                accent: "from-blue-500 to-purple-600",
              },
              {
                title: "Colección Zelda",
                description:
                  "Luce el legendario collar inspirado en la Espada Maestra de Zelda: Tears of the Kingdom. Un accesorio imprescindible para los verdaderos fans de la saga.",
                image: "/productos/collar espada Zelda TOTK.jpg",
                accent: "bg-white",
              },
              {
                title: "Electric Dreams",
                description:
                  "Light up your wardrobe with our Electric Dreams Collection. Vibrant colors for the bold.",
                gradient: "from-yellow-400 to-green-500",
                accent: "bg-yellow-300",
              },
            ].map((collection, index) => (
              <Card
                key={index}
                className={`bg-card border-card-border overflow-hidden group cursor-pointer ${animationClasses.card(
                  index,
                  visibleCards.includes(index)
                )} ${animationClasses.hover}`}
                style={{
                  willChange: prefersReducedMotion
                    ? "auto"
                    : "transform, box-shadow",
                  contain: "layout style paint",
                }}
              >
                <CardContent className="p-0">
                  <div
                    className={
                      `relative h-64 flex items-center justify-center overflow-hidden` +
                      (collection.image ? " bg-cover bg-center" : " bg-gradient-to-br " + collection.gradient)
                    }
                    style={
                      collection.image
                        ? { backgroundImage: `url('${collection.image}')` }
                        : {}
                    }
                  >
                    {!collection.image && (
                      <div
                        className={`w-32 h-32 bg-gradient-to-r ${collection.accent} rounded-lg opacity-80 ${
                          prefersReducedMotion
                            ? ""
                            : "transition-all duration-500 group-hover:scale-110"
                        }`}
                        style={{
                          willChange: prefersReducedMotion ? "auto" : "transform",
                        }}
                      >
                        {index === 1 && collection.image && (
                          <div className="w-full h-full flex items-center justify-center">
                            <img
                              src={collection.image}
                              alt="Collar Zelda"
                              className="object-contain w-20 h-20"
                            />
                          </div>
                        )}
                      </div>
                    )}
                    {!prefersReducedMotion && (
                      <div className="absolute inset-0 bg-asgard-accent/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                    )}
                  </div>
                  <div className="p-6">
                    <h3
                      className={`text-card-title ${
                        prefersReducedMotion
                          ? ""
                          : "group-hover:text-card-title-hover transition-colors duration-300"
                      }`}
                    >
                      {collection.title}
                    </h3>
                    <p
                      className={`text-card-paragraph ${
                        prefersReducedMotion
                          ? ""
                          : "group-hover:text-card-paragraph-hover transition-colors duration-300"
                      }`}
                    >
                      {collection.description}
                    </p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* New Arrivals - Performance Optimized */}
      <section className="px-6 py-16" data-animate id="arrivals">
        <div className="max-w-7xl mx-auto">
          <h2 className={`text-3xl font-bold mb-8 ${animationClasses.hero}`}>
            New Arrivals
          </h2>
          <div className="grid md:grid-cols-4 gap-6">
            {[
              {
                title: "Circuit Board Tee",
                description: "A stylish tee featuring a circuit board design.",
                gradient: "from-green-600 to-green-800",
                content: "<circuit/>",
              },
              {
                title: "Glitch Art Hoodie",
                description: "A comfortable hoodie with a glitch art pattern.",
                gradient: "from-blue-800 to-blue-900",
                content: "🎮",
              },
              {
                title: "Neon Grid Leggings",
                description: "Eye-catching leggings with a neon grid design.",
                gradient: "from-purple-600 to-pink-600",
                content: null,
              },
              {
                title: "Binary Code Scarf",
                description: "A unique scarf with a binary code pattern.",
                gradient: "from-gray-700 to-gray-900",
                content: "01010101",
              },
            ].map((product, index) => (
              <Card
                key={index}
                className={`bg-card border-card-border overflow-hidden group cursor-pointer ${animationClasses.card(
                  index,
                  isLoaded
                )} ${animationClasses.hover}`}
                style={{
                  transitionDelay: prefersReducedMotion
                    ? "0ms"
                    : `${2 + index * 0.1}s`,
                  willChange: prefersReducedMotion
                    ? "auto"
                    : "transform, box-shadow",
                  contain: "layout style paint",
                }}
              >
                <CardContent className="p-0">
                  <div
                    className={`relative h-64 bg-gradient-to-br ${product.gradient} flex items-center justify-center overflow-hidden`}
                  >
                    {product.content && (
                      <div
                        className={`${
                          prefersReducedMotion
                            ? ""
                            : "transition-all duration-500 group-hover:scale-110"
                        }`}
                      >
                        {index === 0 && (
                          <div className="w-20 h-24 bg-green-400 rounded-lg flex items-center justify-center">
                            <div
                              className={`text-xs text-green-900 font-mono ${
                                prefersReducedMotion ? "" : "animate-pulse"
                              }`}
                            >
                              {product.content}
                            </div>
                          </div>
                        )}
                        {index === 1 && (
                          <div className="w-24 h-28 bg-blue-600 rounded-lg flex items-center justify-center">
                            <div
                              className={`text-white text-lg ${
                                prefersReducedMotion ? "" : "animate-bounce"
                              }`}
                            >
                              {product.content}
                            </div>
                          </div>
                        )}
                        {index === 3 && (
                          <div className="w-28 h-8 bg-gray-600 rounded-full flex items-center justify-center">
                            <div
                              className={`text-xs text-white font-mono ${
                                prefersReducedMotion ? "" : "animate-pulse"
                              }`}
                            >
                              {product.content}
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                    {index === 2 && (
                      <div
                        className={`w-16 h-32 bg-gradient-to-b from-purple-400 to-pink-400 rounded-lg ${
                          prefersReducedMotion
                            ? ""
                            : "transition-all duration-500 group-hover:scale-110"
                        }`}
                      ></div>
                    )}
                    {/* Optimized shimmer effect - disabled on mobile for performance */}
                    {!prefersReducedMotion && !isMobile && (
                      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
                    )}
                  </div>
                  <div className="p-4">
                    <h3
                      className={`font-bold mb-1 ${
                        prefersReducedMotion
                          ? ""
                          : "group-hover:text-card-title transition-colors duration-300"
                      }`}
                    >
                      {product.title}
                    </h3>
                    <p
                      className={`text-card-paragraph ${
                        prefersReducedMotion
                          ? ""
                          : "group-hover:text-card-paragraph-hover transition-colors duration-300"
                      }`}
                    >
                      {product.description}
                    </p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Community Section - Simplified for mobile */}
      <section className="px-6 py-16 text-center" data-animate id="community">
        <div className={`max-w-4xl mx-auto ${animationClasses.hero}`}>
          <h2
            className={`text-4xl font-bold mb-4 ${
              prefersReducedMotion
                ? "text-white"
                : "bg-gradient-to-r from-white via-asgard-accent to-cyan-400 bg-clip-text text-transparent animate-pulse"
            }`}
          >
            Únete a la Comunidad AsgardStore
          </h2>
          <p
            className={`text-card-paragraph text-lg mb-8 ${
              prefersReducedMotion ? "" : "animate-pulse"
            }`}
          >
            Estate Atento a Diseños Nuevos
          </p>
          <Button
            className={`bg-asgard-purple hover:bg-asgard-purple-hover text-white hover:shadow-[0_4px_24px_0_rgba(120,71,235,0.5)] px-8 py-3 text-lg relative overflow-hidden group ${
              prefersReducedMotion
                ? ""
                : isMobile
                ? "active:scale-95 transition-transform duration-150"
                : "transition-all duration-300 hover:scale-110 hover:shadow-xl hover:shadow-asgard-accent/50"
            }`}
            style={{ willChange: prefersReducedMotion ? "auto" : "transform" }}
          >
            <span className="relative z-10">Registrarse</span>
            {!prefersReducedMotion && !isMobile && (
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-asgard-accent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            )}
          </Button>
        </div>
      </section>

      {/* Footer - Simplified animations */}
      <footer
        className={`border-t border-asgard-purple px-6 py-8 ${animationClasses.hero}`}
      >
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-wrap justify-between items-center mb-8">
            <div className="flex flex-wrap space-x-8">
              {[
                "Acerca de Nosotros",
                "Contacto",
                "FAQ",
                "Políticas de Privacidad",
                "Términos de Servicio",
              ].map((link, index) => (
                <a
                  key={link}
                  href="#"
                  className={`text-card-paragraph ${
                    prefersReducedMotion ? "" : "transition-all duration-300"
                  }`}
                >
                  {link}
                  {!prefersReducedMotion && (
                    <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-asgard-accent transition-all duration-300 group-hover:w-full"></span>
                  )}
                </a>
              ))}
            </div>
            <div className="flex space-x-4 mt-4 md:mt-0">
              {["T", "I", "F"].map((social, index) => (
                <div
                  key={social}
                  className={`w-6 h-6 bg-asgard-light-purple rounded-full flex items-center justify-center cursor-pointer ${
                    prefersReducedMotion
                      ? "hover:bg-asgard-accent"
                      : isMobile
                      ? "active:scale-95 transition-all duration-150"
                      : "transition-all duration-300 hover:bg-asgard-accent hover:scale-110"
                  }`}
                  style={{
                    willChange: prefersReducedMotion ? "auto" : "transform",
                  }}
                >
                  <span className="text-xs text-white">{social}</span>
                </div>
              ))}
            </div>
          </div>
          <div
            className={`text-center text-card-paragraph text-sm ${
              prefersReducedMotion ? "" : "animate-pulse"
            }`}
          >
            © 2024 Asgard_Store. Todos los Derechos Reservados.
          </div>
        </div>
      </footer>

      {/* Optimized loading overlay */}
      {!isLoaded && (
        <div className="fixed inset-0 bg-asgard-dark z-50 flex items-center justify-center">
          <div className="text-center">
            <div
              className={`w-16 h-16 border-4 border-asgard-accent border-t-transparent rounded-full mb-4 ${
                prefersReducedMotion ? "" : "animate-spin"
              }`}
            ></div>
            <p
              className={`text-card-paragraph ${
                prefersReducedMotion ? "" : "animate-pulse"
              }`}
            >
              Cargando Asgard Store...
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
