const features = [
  {
    title: "Security First",
    description: "Advanced biometric authentication and end-to-end encryption protect your financial data.",
    image: "/biometric-banking-security.png",
  },
  {
    title: "Your Money, Your Way",
    description: "Customizable account controls and spending limits give you complete financial autonomy.",
    image: "/mobile-banking-controls.png",
  },
  {
    title: "Always Transparent",
    description: "No hidden fees, clear statements, and real-time notifications keep you informed.",
    image: "/transparent-banking-statements.png",
  },
]

export function FeatureHighlights() {
  return (
    <section className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-6">
        <div className="space-y-16">
          {features.map((feature, index) => (
            <div
              key={feature.title}
              className={`grid md:grid-cols-2 gap-12 items-center ${index % 2 === 1 ? "md:grid-flow-col-dense" : ""}`}
            >
              <div className={index % 2 === 1 ? "md:col-start-2" : ""}>
                <h3 className="text-3xl md:text-4xl font-bold text-[#334155] mb-6">{feature.title}</h3>
                <p className="text-lg text-[#334155] leading-relaxed">{feature.description}</p>
              </div>
              <div className={`group ${index % 2 === 1 ? "md:col-start-1" : ""}`}>
                <img
                  src={feature.image || "/placeholder.svg"}
                  alt={feature.title}
                  className="w-full h-auto rounded-lg shadow-lg group-hover:shadow-xl transition-all duration-300 group-hover:scale-105"
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
