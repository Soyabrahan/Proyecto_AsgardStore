import { motion, HTMLMotionProps } from "framer-motion";
import { ReactNode } from "react";

// Variantes de animación reutilizables
export const fadeInUp = {
  initial: { opacity: 0, y: 60 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: 60 },
};

export const fadeInDown = {
  initial: { opacity: 0, y: -60 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -60 },
};

export const fadeInLeft = {
  initial: { opacity: 0, x: -60 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: -60 },
};

export const fadeInRight = {
  initial: { opacity: 0, x: 60 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: 60 },
};

export const scaleIn = {
  initial: { opacity: 0, scale: 0.8 },
  animate: { opacity: 1, scale: 1 },
  exit: { opacity: 0, scale: 0.8 },
};

export const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.1,
    },
  },
};

// Componentes de animación reutilizables
interface AnimatedDivProps extends HTMLMotionProps<"div"> {
  children: ReactNode;
  variant?:
    | "fadeInUp"
    | "fadeInDown"
    | "fadeInLeft"
    | "fadeInRight"
    | "scaleIn";
  delay?: number;
}

export function AnimatedDiv({
  children,
  variant = "fadeInUp",
  delay = 0,
  ...props
}: AnimatedDivProps) {
  const variants = {
    fadeInUp,
    fadeInDown,
    fadeInLeft,
    fadeInRight,
    scaleIn,
  };

  return (
    <motion.div
      variants={variants[variant]}
      initial="initial"
      animate="animate"
      exit="exit"
      transition={{ delay, duration: 0.6, ease: "easeOut" }}
      {...props}
    >
      {children}
    </motion.div>
  );
}

interface StaggerContainerProps extends HTMLMotionProps<"div"> {
  children: ReactNode;
}

export function StaggerContainer({
  children,
  ...props
}: StaggerContainerProps) {
  return (
    <motion.div
      variants={staggerContainer}
      initial="initial"
      animate="animate"
      {...props}
    >
      {children}
    </motion.div>
  );
}

// Animación para elementos que aparecen al hacer scroll
export const scrollReveal = {
  hidden: { opacity: 0, y: 75 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.6,
      ease: "easeOut",
    },
  },
};

// Hook personalizado para animaciones de scroll
export function useScrollAnimation() {
  return {
    variants: scrollReveal,
    initial: "hidden",
    whileInView: "visible",
    viewport: { once: true, amount: 0.3 },
  };
}

// Animación para botones con hover
export const buttonHover = {
  scale: 1.05,
  transition: { duration: 0.2, ease: "easeInOut" },
};

export const buttonTap = {
  scale: 0.95,
  transition: { duration: 0.1, ease: "easeInOut" },
};

// Animación para cards
export const cardHover = {
  y: -10,
  transition: { duration: 0.3, ease: "easeOut" },
};

// Animación para loading
export const loadingPulse = {
  scale: [1, 1.1, 1],
  opacity: [0.5, 1, 0.5],
  transition: {
    duration: 1.5,
    repeat: Infinity,
    ease: "easeInOut",
  },
};
