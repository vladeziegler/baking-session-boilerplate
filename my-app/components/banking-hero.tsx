import { Button } from "@/components/ui/button"

export function BankingHero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center px-6 overflow-hidden">
      {/* Background animated graph */}
      <div className="absolute inset-0 opacity-5">
        <svg className="w-full h-full" viewBox="0 0 800 600">
          <path
            d="M0,300 Q200,200 400,250 T800,200"
            stroke="#2563eb"
            strokeWidth="2"
            fill="none"
            className="animate-float"
          />
          <path
            d="M0,350 Q200,280 400,300 T800,250"
            stroke="#0ea5e9"
            strokeWidth="1.5"
            fill="none"
            className="animate-float"
            style={{ animationDelay: "2s" }}
          />
        </svg>
      </div>

      <div className="relative z-10 text-center max-w-4xl mx-auto">
        <h1 className="text-5xl md:text-7xl font-bold text-[#334155] mb-6 leading-tight">
          Banking, Simplified.
          <br />
          <span className="text-[#2563eb]">Trust, Guaranteed.</span>
        </h1>

        <p className="text-xl md:text-2xl text-[#334155] mb-12 max-w-2xl mx-auto leading-relaxed">
          A modern banking experience built for security, clarity, and control over your finances.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Button
            size="lg"
            className="bg-[#2563eb] hover:bg-[#0ea5e9] text-white px-8 py-4 text-lg font-semibold transition-all duration-200 hover:translate-y-[-2px] shadow-lg hover:shadow-xl"
          >
            Open an Account
          </Button>
          <button className="text-[#2563eb] hover:text-[#0ea5e9] text-lg font-medium underline decoration-2 underline-offset-4 hover:underline-offset-8 transition-all duration-200">
            Learn More
          </button>
        </div>
      </div>
    </section>
  )
}
