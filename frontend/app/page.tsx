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

  return (
    <div className="min-h-screen bg-[#171221] text-white overflow-x-hidden">
      {/* Header - Optimized */}
      <header
        className={`border-b border-[#2e2447] px-6 py-4 ${animationClasses.header}`}
      >
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-8">
            <div className="flex items-center space-x-2 group">
              <span
                className={`w-8 h-8 inline-block align-middle text-white ${
                  prefersReducedMotion
                    ? ""
                    : "transition-colors duration-300 group-hover:text-[#FFD700]"
                }`}
                style={{ willChange: prefersReducedMotion ? "auto" : "color" }}
                aria-label="Logo Asgard Store"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 548.27 497.64"
                  width="32"
                  height="29"
                  fill="currentColor"
                >
                  <g id="Capa_x0020_1">
                    <path
                      className="fil0"
                      d="M265.09 170.81c0,6.09 7.05,11.8 8.52,18.1 4.94,-0.41 3.97,-1.86 8.98,-10.18l52.77 -88.82c3.04,2.23 9.33,14.66 11.92,18.96l58.56 100.07c4.14,6.91 7.6,13.52 11.55,20.38l75.48 129.99c4.91,8.59 27.7,46.32 28.8,51.05l-115.06 0.06c-4.97,1.01 -3.33,1.51 -1.63,4.61 1.41,2.57 2.56,3.97 3.78,6.05 3.04,5.17 3.5,8.45 11.77,8.45l118.17 0c7.14,0 9.58,-5.29 9.58,-10.65 0,-4.47 -3.61,-7.68 -5.66,-11.37 -2.45,-4.41 -4.14,-7.15 -6.67,-11.43 -2.51,-4.25 -3.97,-7.38 -6.5,-11.6 -2.41,-4.03 -4.72,-7.47 -6.73,-11.37l-12.83 -22.3c-19.94,-33.06 -39.17,-68.92 -58.95,-101.8 -2.56,-4.26 -4.22,-7.07 -6.66,-11.44 -20.28,-36.29 -45.41,-75.9 -65.6,-112.19 -9.84,-17.68 -23.7,-39.65 -32.65,-56.77 -11.5,-21.99 -24.73,8.46 -30.29,17.65 -12.96,21.41 -33.54,58.75 -45.94,77.56 -0.72,1.09 -4.7,6.83 -4.7,7.01zm101.67 80.91c0.02,-2.96 0.52,-0.81 -0.55,-3.24 -2.07,-4.69 -0.48,-1.56 -2.11,-2.09 -0.84,-2.54 -0.05,-1.22 -1.43,-3.82 -1.24,-2.32 -0.82,-1.41 -1.76,-2.3 -1.48,-3.2 -6.26,-12.36 -8.52,-14.11 -1.4,-4.21 -5.86,-11.53 -8.31,-14.9 -1.5,-2.32 -2.15,-4.11 -3.45,-6.35 -5.26,-9.1 -23.83,-42.2 -27.64,-44.75 -3.97,2.66 -10.62,15.75 -10.65,15.97l21.29 36.2c1.01,3.03 0.59,1.88 1.89,4.53 0.02,0.04 1.69,3.15 1.87,3.44 1.8,2.94 2.29,3.05 4.06,6.56 1.71,3.39 5.82,11.42 8.1,13.14 0.55,2.14 0.4,2.08 1.52,3.93 2.78,4.6 1.63,2.09 2.79,2.51 0.74,4.08 2.02,5.45 3.93,8.8 1.4,2.45 2.94,5.1 4.33,7.11l25.45 44.01c2.21,4.05 3.78,6.9 6.14,10.89l12.65 21.42c2.83,5.07 5.76,8.39 6.06,12.04l-201.15 0.06c-5.59,0.97 -11.51,14.88 -11.77,18.03 67.78,0 135.56,0 203.34,0 46.35,0 44.05,1.12 16.58,-45.33 -4.52,-7.64 -34.51,-61.24 -37.87,-63.85 -0.49,-2.53 -0.24,-2.38 -1.31,-4.46 -1.93,-3.75 -0.13,-1.63 -3.47,-3.46zm-91.03 6.39c1.67,5.01 3.98,8.39 6.39,12.66l37.26 63.98 20.23 0c-0.14,-6.08 -19.36,-36.01 -22.72,-42.22l-24.13 -40.92c-1.28,-2.28 -2.16,-3.48 -3.47,-5.96 -0.77,-1.45 -0.63,-1.71 -1.45,-2.81 -2.2,-2.93 0.04,-1.22 -3.48,-2.83 0.83,-4.23 -2.48,-6.5 -6.86,-14.54l-12.21 -20.79c-8.45,-13.01 -27.71,-48.29 -37.01,-64.13 -3.24,-5.51 -3.77,-10.36 -12.17,-10.37 -7.1,-0.01 -7.57,2.13 -12.08,10.46 -2.74,5.06 -5.45,9.14 -8.36,13.99l-8.31 14.05c-10.83,20.18 -29.63,48.29 -39.52,66.99 -2.13,4.03 -1.46,0.56 -1.36,4.34 -2.19,1.68 -0.33,-0.01 -1.86,1.84l-5.12 7.78c-2.34,4.09 -3.9,6.83 -6.43,10.6l-41.87 70.18c-1.34,3.48 -1.4,3.49 2.41,4.3 2.44,0.52 14.73,0.04 18.16,0.04 1.12,-4.81 3.5,-7.14 5.94,-11.1l19.41 -32.75c10.06,-16.7 76.55,-126.99 77.92,-132.88l23.47 38.27c2.4,4.2 5.29,8.07 7.73,12.49 2.62,4.74 4.79,7.7 7.12,12.04l10.85 18.96c2.77,4.27 9.72,17.36 11.51,18.31zm-50.51 15.96c4.06,-3.4 4.87,-6.74 8.08,-11.56 1.08,-1.62 1.29,-2.09 2.35,-4.04 1.73,-3.18 2.81,-4.92 4.62,-8.16 1.68,-3.01 3.66,-4.88 4.59,-7.86 3.59,-5.82 -5.34,-10.42 -7.45,-19.48 -4.94,0.41 -2.81,-0.14 -8.18,8.85l-97.83 165.13c-2.68,4.53 -12.11,18.91 -12.25,23.05 -0.38,11.55 14.47,9.5 25.64,9.5l140.53 0c17.04,0 56.02,2.01 69.2,-1.06 -0.4,-4.81 -7.07,-16.41 -10.08,-17.6 -3.88,-1.53 -188.72,-0.5 -197.52,-0.5 0.42,-5.11 15.69,-28.15 19.11,-34.12 6.68,-11.68 13.1,-22.66 20.09,-34.21l9.83 -16.79c3.12,-5.46 6.41,-10.98 9.86,-16.75 2.53,-4.22 19.18,-29.37 19.42,-34.4zm-225.22 85.17c0,6.59 5.7,9.58 7.45,9.58l121.37 0c3.57,0 3.7,-3.68 7.8,-10.32 6.53,-10.57 7.75,-7.78 -38.67,-7.78 -24.13,0 -48.26,0 -72.39,0 0.91,-3.41 8.8,-14.84 11.71,-20.23l83.09 -140.48c3.83,-6.7 7.97,-12.76 11.99,-19.95 2.28,-4.08 3.9,-6.46 6.01,-9.96l17.68 -30.23c1.23,-2.04 1.63,-2.8 2.81,-4.64l39.14 -65.2c2.21,-3.82 3.15,-6.2 5.79,-10.18 2.43,-3.66 3.66,-6.61 5.95,-10.02 2.15,-3.2 4.32,-6.32 5.32,-10.65 4.09,1.09 2.54,0.84 4.66,4.92 5.54,10.64 50.24,88.45 53.89,90.9 2.73,-1.82 3.74,-4.24 5.54,-7.23 7.56,-12.6 3.38,-11.87 -3.06,-23.99 -1.55,-2.92 -2.03,-4.27 -3.75,-6.9 -1.94,-2.97 -2.6,-3.91 -4.42,-7.29l-40.09 -68.5c-3.27,-4.93 -11.43,-20.36 -21.37,-3.27l-20.15 34.15c-2.45,3.66 -4.26,7.27 -6.72,11.37 -2.49,4.14 -4.13,7.28 -6.65,11.45l-153.83 259.24c-3.96,6.58 -19.1,30.51 -19.1,35.19zm0 127.75c0,5.36 2.44,10.65 9.58,10.65l409.87 0c4.36,0 9.58,-3.12 9.58,-9.58 0,-4.88 -4.55,-9.58 -6.72,-13.5l-45.39 -78.11c-8,-14 -4.2,-11.66 -26.67,-11.66 0.15,6.61 8.78,18.09 12.08,24.12l16.37 28.34c4.93,7.35 22.37,37.84 22.65,41.23l-374.74 0c1.21,-4.54 10.14,-18.1 13.11,-23.09l34.07 -57.49c3.63,-6.56 5.94,-8.07 6.05,-13.11 -26.23,0 -17.83,-4.1 -34.67,23.88l-30.6 51.38c-2.41,4.32 -14.58,22.72 -14.58,26.94z"
                    />
                  </g>
                </svg>
              </span>
              <span
                className={`text-xl font-bold ${
                  prefersReducedMotion
                    ? ""
                    : "transition-colors duration-300 group-hover:text-[#7847eb]"
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
                    className={`text-[#a394c7] hover:text-white relative group ${
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
                      <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-[#7847eb] transition-all duration-300 group-hover:w-full"></span>
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
                className={`absolute left-3 top-1/2 transform -translate-y-1/2 text-[#a394c7] w-4 h-4 ${
                  prefersReducedMotion
                    ? ""
                    : "transition-colors duration-300 group-focus-within:text-[#7847eb]"
                }`}
              />
              <Input
                placeholder="Buscar"
                className={`pl-10 bg-[#2e2447] border-[#2e2447] text-white placeholder:text-[#a394c7] w-64 ${
                  prefersReducedMotion
                    ? ""
                    : "transition-all duration-300 focus:border-[#7847eb] focus:ring-2 focus:ring-[#7847eb]/20"
                }`}
              />
            </div>
            <Button
              variant="outline"
              className={`border-[#7847eb] text-[#7847eb] hover:bg-[#7847eb] hover:text-white bg-transparent ${
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
                  {[...Array(particleCount)].map((_, i) => (
                    <div
                      key={i}
                      className="absolute w-1 h-1 bg-cyan-300 rounded-full"
                      style={{
                        left: `${Math.random() * 100}%`,
                        top: `${Math.random() * 100}%`,
                        animation: `ping ${2 + Math.random() * 2}s infinite ${
                          Math.random() * 3
                        }s`,
                        willChange: "transform, opacity",
                      }}
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
                      className={`inline-block text-[#7847eb] ${
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
                    className={`text-xl text-[#e5e8eb] mb-8 ${animationClasses.hero}`}
                  >
                    Armate y expresa tu estilo con ropa inspirada en la cultura
                    Geek
                  </p>
                  <Button
                    className={`bg-[#7847eb] hover:bg-[#7847eb]/90 text-white px-8 py-3 text-lg ${
                      prefersReducedMotion
                        ? ""
                        : isMobile
                        ? "active:scale-95 transition-transform duration-150"
                        : "transition-all duration-300 hover:scale-110 hover:shadow-xl hover:shadow-[#7847eb]/50"
                    }`}
                    style={{
                      willChange: prefersReducedMotion ? "auto" : "transform",
                    }}
                  >
                    Comprar
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
                title: "Billetera R2-D2",
                description:
                  "Lleva la galaxia contigo con esta billetera inspirada en R2-D2, perfecta para fans de Star Wars.",
                image: "/productos/billetera R2-D2.jpg",
                accent: "from-blue-300 to-gray-400",
              },
              {
                title: "Collar Espada Zelda",
                description:
                  "Porta la leyenda con el collar de la Espada Maestra de Zelda: Tears of the Kingdom. Un accesorio imprescindible para gamers.",
                image: "/productos/collar espada Zelda TOTK.jpg",
                accent: "from-green-400 to-blue-500",
              },
            ].map((collection, index) => (
              <Card
                key={index}
                className={`bg-[#2e2447] border-[#2e2447] overflow-hidden group cursor-pointer ${animationClasses.card(
                  index,
                  visibleCards.includes(index)
                )} ${animationClasses.hover} transition-all duration-500 `}
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
                      (collection.image
                        ? " bg-black"
                        : " bg-gradient-to-br " + collection.accent)
                    }
                  >
                    {collection.image && (
                      <img
                        src={collection.image}
                        alt={collection.title}
                        className="object-cover w-full h-full absolute inset-0 z-0"
                      />
                    )}
                    {/* Si no hay imagen, mostramos el gradiente como antes */}
                    {!collection.image && (
                      <div
                        className={`w-32 h-32 bg-gradient-to-r ${
                          collection.accent
                        } rounded-lg opacity-80 ${
                          prefersReducedMotion
                            ? ""
                            : "transition-all duration-500 group-hover:scale-110"
                        }`}
                        style={{
                          willChange: prefersReducedMotion
                            ? "auto"
                            : "transform",
                        }}
                      >
                        {index === 1 && (
                          <div className="w-full h-full flex items-center justify-center">
                            <div
                              className={`text-2xl font-bold text-gray-800 ${
                                prefersReducedMotion ? "" : "animate-bounce"
                              }`}
                            >
                              👕
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                    {!prefersReducedMotion && (
                      <div className="absolute inset-0 bg-[#7847eb]/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                    )}
                  </div>
                  <div className="p-6">
                    <h3
                      className={`text-xl font-bold mb-2 ${
                        prefersReducedMotion
                          ? ""
                          : "group-hover:text-[#7847eb] transition-colors duration-300"
                      }`}
                    >
                      {collection.title}
                    </h3>
                    <p
                      className={`text-[#a394c7] text-sm ${
                        prefersReducedMotion
                          ? ""
                          : "group-hover:text-white transition-colors duration-300"
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
            Mercancia Nueva
          </h2>
          <div className="grid md:grid-cols-4 gap-6">
            {[
              {
                title: "Franela Retro 8bits",
                description:
                  "Revive la nostalgia de los videojuegos clásicos con esta franela de estilo retro 8bits.",
                image: "/productos/franela Retro 8bits.jpg",
                gradient: "from-pink-400 to-yellow-400",
              },
              {
                title: "Gorra Venom",
                description:
                  "Demuestra tu lado más audaz con la gorra inspirada en Venom. Ideal para los fans de los cómics.",
                image: "/productos/gorra venom.jpg",
                gradient: "from-black to-purple-900",
              },
              {
                title: "Medias Matrix",
                description:
                  "Sumérgete en el código con estas medias inspiradas en Matrix. Perfectas para los amantes de la ciencia ficción.",
                image: "/productos/medias Matrix.jpg",
                gradient: "from-green-700 to-black",
              },
              {
                title: "Suéter Armadura Medieval",
                description:
                  "Luce como un verdadero caballero con este suéter de armadura medieval. Para los fans de la fantasía épica.",
                image: "/productos/sueter armadura medieval.jpeg",
                gradient: "from-gray-500 to-gray-900",
              },
            ].map((product, index) => (
              <Card
                key={index}
                className={`bg-[#2e2447] border-[#2e2447] overflow-hidden group cursor-pointer ${animationClasses.card(
                  index,
                  visibleCards.includes(index)
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
                    className={`relative h-64 bg-gradient-to-br ${product.gradient} flex items-center justify-center overflow-hidden transition-all duration-500 group-hover:scale-110`}
                  >
                    {product.image && (
                      <img
                        src={product.image}
                        alt={product.title}
                        className="object-cover w-full h-full absolute inset-0 z-0"
                      />
                    )}
                    {!prefersReducedMotion && (
                      <div className="absolute inset-0 bg-[#7847eb]/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                    )}
                  </div>
                  <div className="p-4">
                    <h3
                      className={`font-bold mb-1 ${
                        prefersReducedMotion
                          ? ""
                          : "group-hover:text-[#7847eb] transition-colors duration-300"
                      }`}
                    >
                      {product.title}
                    </h3>
                    <p
                      className={`text-[#a394c7] text-sm ${
                        prefersReducedMotion
                          ? ""
                          : "group-hover:text-white transition-colors duration-300"
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
                : "bg-gradient-to-r from-white via-[#7847eb] to-cyan-400 bg-clip-text text-transparent animate-pulse"
            }`}
          >
            Únete a la Comunidad AsgardStore
          </h2>
          <p
            className={`text-[#a394c7] text-lg mb-8 ${
              prefersReducedMotion ? "" : "animate-pulse"
            }`}
          >
            Estate Atento a Diseños Nuevos
          </p>
          <Button
            className={`bg-[#7847eb] hover:bg-[#7847eb]/90 text-white px-8 py-3 text-lg relative overflow-hidden group ${
              prefersReducedMotion
                ? ""
                : isMobile
                ? "active:scale-95 transition-transform duration-150"
                : "transition-all duration-300 hover:scale-110 hover:shadow-xl hover:shadow-[#7847eb]/50"
            }`}
            style={{ willChange: prefersReducedMotion ? "auto" : "transform" }}
          >
            <span className="relative z-10">Registrarse</span>
            {!prefersReducedMotion && !isMobile && (
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-purple-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            )}
          </Button>
        </div>
      </section>

      {/* Footer - Simplified animations */}
      <footer
        className={`border-t border-[#2e2447] px-6 py-8 ${animationClasses.hero}`}
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
                  className={`text-[#a394c7] hover:text-white relative group ${
                    prefersReducedMotion ? "" : "transition-all duration-300"
                  }`}
                >
                  {link}
                  {!prefersReducedMotion && (
                    <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-[#7847eb] transition-all duration-300 group-hover:w-full"></span>
                  )}
                </a>
              ))}
            </div>
            <div className="flex space-x-4 mt-4 md:mt-0">
              {["T", "I", "F"].map((social, index) => (
                <div
                  key={social}
                  className={`w-6 h-6 bg-[#a394c7] rounded-full flex items-center justify-center cursor-pointer ${
                    prefersReducedMotion
                      ? "hover:bg-[#7847eb]"
                      : isMobile
                      ? "active:scale-95 transition-all duration-150 hover:bg-[#7847eb]"
                      : "transition-all duration-300 hover:bg-[#7847eb] hover:scale-110"
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
            className={`text-center text-[#a394c7] text-sm ${
              prefersReducedMotion ? "" : "animate-pulse"
            }`}
          >
            © 2024 Asgard_Store. Todos los Derechos Reservados.
          </div>
        </div>
      </footer>

      {/* Optimized loading overlay */}
      {!isLoaded && (
        <div className="fixed inset-0 bg-[#171221] z-50 flex items-center justify-center">
          <div className="text-center">
            <div
              className={`w-16 h-16 border-4 border-[#7847eb] border-t-transparent rounded-full mb-4 ${
                prefersReducedMotion ? "" : "animate-spin"
              }`}
            ></div>
            <p
              className={`text-[#a394c7] ${
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
