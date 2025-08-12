"use client"

import { useEffect, useState } from "react"

const partners = [
  { name: "Visa", logo: "/visa-logo-generic.png" },
  { name: "Mastercard", logo: "/mastercard-logo.png" },
  { name: "FDIC Insured", logo: "/fdic-insured-logo.png" },
  { name: "PCI DSS Certified", logo: "/placeholder-dg38w.png" },
]

export function TrustSignals() {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true)
        }
      },
      { threshold: 0.1 },
    )

    const element = document.getElementById("trust-signals")
    if (element) observer.observe(element)

    return () => observer.disconnect()
  }, [])

  return (
    <section id="trust-signals" className="py-16 bg-[#f8fafc]">
      <div className="max-w-6xl mx-auto px-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 items-center justify-items-center">
          {partners.map((partner, index) => (
            <div
              key={partner.name}
              className={`opacity-0 ${isVisible ? "animate-slide-in-up" : ""}`}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <img
                src={partner.logo || "/placeholder.svg"}
                alt={partner.name}
                className="h-10 w-auto grayscale hover:grayscale-0 transition-all duration-300"
              />
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
