import Link from "next/link";
import {
  ClipboardCheck,
  FileText,
  LayoutDashboard,
  RadioTower,
} from "lucide-react";

const navigation = [
  { href: "/", label: "Overview", icon: LayoutDashboard },
  { href: "/channels", label: "Channels", icon: RadioTower },
  { href: "/validations", label: "Validations", icon: ClipboardCheck },
  { href: "/reports", label: "Reports", icon: FileText },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-line bg-surface/92 px-5 py-5 lg:block">
        <Link href="/" className="block rounded-md px-2 py-1">
          <p className="text-sm font-medium text-muted">MarketMaster</p>
          <h1 className="mt-2 text-xl font-semibold">Validation Command</h1>
        </Link>
        <nav className="mt-8 space-y-1" aria-label="Primary">
          {navigation.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium text-muted hover:bg-surface-strong hover:text-foreground"
            >
              <item.icon aria-hidden="true" size={18} />
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="absolute bottom-5 left-5 right-5 rounded-lg border border-accent-2/35 bg-accent-2/10 p-4">
          <p className="text-sm font-medium text-accent-2">Sell gate blocked</p>
          <p className="mt-2 text-sm leading-6 text-muted">
            Repo validation system is complete. Live account evidence is still required.
          </p>
        </div>
      </aside>

      <div className="lg:pl-64">
        <header className="sticky top-0 z-20 border-b border-line bg-background/92 px-4 py-3 backdrop-blur md:px-8">
          <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
            <div>
              <p className="text-xs font-medium uppercase text-muted">
                Distribution Engine
              </p>
              <p className="text-sm text-foreground">
                Validation system implemented; commercial proof pending.
              </p>
            </div>
            <nav className="flex flex-wrap gap-2 lg:hidden" aria-label="Mobile">
              {navigation.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className="inline-flex items-center gap-2 rounded-md border border-line px-3 py-2 text-sm text-muted"
                >
                  <item.icon aria-hidden="true" size={16} />
                  {item.label}
                </Link>
              ))}
            </nav>
          </div>
        </header>
        <main className="mx-auto w-full max-w-7xl px-4 py-6 md:px-8 md:py-8">
          {children}
        </main>
      </div>
    </div>
  );
}
