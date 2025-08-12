import { BankingHero } from "@/components/banking-hero"
import { TrustSignals } from "@/components/trust-signals"
import { FeatureHighlights } from "@/components/feature-highlights"
import { RateSnapshot } from "@/components/rate-snapshot"
import { ClosingCTA } from "@/components/closing-cta"
import { ChatBot } from "@/components/chatbot"

export default function HomePage() {
  return (
    <main className="min-h-screen bg-white">
      <BankingHero />
      <TrustSignals />
      <FeatureHighlights />
      <RateSnapshot />
      <ClosingCTA />
      <ChatBot />
    </main>
  )
}
