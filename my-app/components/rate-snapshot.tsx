"use client"

import { useState, useEffect } from "react"

const rates = {
  personal: [
    { type: "Savings APY", rate: "4.50%" },
    { type: "Checking APY", rate: "2.25%" },
    { type: "Personal Loan", rate: "6.99%" },
    { type: "Mortgage Rate", rate: "7.25%" },
  ],
  business: [
    { type: "Business Savings", rate: "4.75%" },
    { type: "Business Checking", rate: "2.50%" },
    { type: "Business Loan", rate: "8.99%" },
    { type: "Commercial Mortgage", rate: "7.75%" },
  ],
}

export function RateSnapshot() {
  const [activeTab, setActiveTab] = useState<"personal" | "business">("personal")
  const [animatedRates, setAnimatedRates] = useState<Record<string, number>>({})

  useEffect(() => {
    const currentRates = rates[activeTab]
    const newAnimatedRates: Record<string, number> = {}

    currentRates.forEach((item) => {
      const targetValue = Number.parseFloat(item.rate.replace("%", ""))
      let currentValue = 0
      const increment = targetValue / 30

      const animate = () => {
        currentValue += increment
        if (currentValue >= targetValue) {
          newAnimatedRates[item.type] = targetValue
          setAnimatedRates({ ...newAnimatedRates })
        } else {
          newAnimatedRates[item.type] = currentValue
          setAnimatedRates({ ...newAnimatedRates })
          requestAnimationFrame(animate)
        }
      }
      animate()
    })
  }, [activeTab])

  return (
    <section className="py-24 bg-[#f8fafc]">
      <div className="max-w-4xl mx-auto px-6">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-[#334155] mb-4">Competitive Rates</h2>
          <p className="text-lg text-[#334155]">Transparent pricing with no hidden fees</p>
        </div>

        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="flex border-b">
            <button
              onClick={() => setActiveTab("personal")}
              className={`flex-1 py-4 px-6 text-lg font-semibold transition-colors ${
                activeTab === "personal" ? "bg-[#2563eb] text-white" : "text-[#334155] hover:bg-gray-50"
              }`}
            >
              Personal
            </button>
            <button
              onClick={() => setActiveTab("business")}
              className={`flex-1 py-4 px-6 text-lg font-semibold transition-colors ${
                activeTab === "business" ? "bg-[#2563eb] text-white" : "text-[#334155] hover:bg-gray-50"
              }`}
            >
              Business
            </button>
          </div>

          <div className="p-6">
            <div className="grid md:grid-cols-2 gap-6">
              {rates[activeTab].map((item) => (
                <div key={item.type} className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                  <span className="font-medium text-[#334155]">{item.type}</span>
                  <span className="text-2xl font-bold text-[#2563eb] tabular-nums">
                    {animatedRates[item.type]?.toFixed(2) || "0.00"}%
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
