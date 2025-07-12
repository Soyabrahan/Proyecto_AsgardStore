import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Asgard Store - Análisis Predictivo',
  description: 'Tienda de ropa con análisis predictivo de tendencias usando machine learning',
  generator: 'Next.js',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
