import { ConnectorCard } from "@/components/connector-card";
import { connectors } from "@/lib/validation/tracker";

export default function ChannelsPage() {
  return (
    <div className="space-y-6">
      <section className="border-b border-line pb-6">
        <p className="text-sm font-medium text-accent-3">Connector matrix</p>
        <h1 className="mt-2 text-3xl font-semibold">
          Live access and fallback status
        </h1>
        <p className="mt-4 max-w-4xl text-base leading-7 text-muted">
          Each channel records the exact live action, credential dependency,
          and manual fallback. Nothing is marked live until account-backed
          execution evidence exists.
        </p>
      </section>
      <section className="grid gap-4 lg:grid-cols-2">
        {connectors.map((connector) => (
          <ConnectorCard key={connector.id} connector={connector} />
        ))}
      </section>
    </div>
  );
}
