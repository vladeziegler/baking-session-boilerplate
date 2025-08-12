import { Button } from "@/components/ui/button"

export function ClosingCTA() {
  return (
    <section className="py-24 bg-white">
      <div className="max-w-4xl mx-auto px-6 text-center">
        <h2 className="text-3xl md:text-5xl font-bold text-[#334155] mb-6">
          Join thousands who trust us with their future.
        </h2>
        <p className="text-lg text-[#334155] mb-12 max-w-2xl mx-auto">
          Experience banking that puts your security, transparency, and financial goals first.
        </p>
        <Button
          size="lg"
          className="bg-[#2563eb] hover:bg-[#0ea5e9] text-white px-12 py-4 text-xl font-semibold transition-all duration-200 hover:translate-y-[-2px] shadow-lg hover:shadow-xl"
        >
          Get Started
        </Button>
      </div>
    </section>
  )
}
