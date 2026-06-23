import { ValidationTable } from "@/components/validation-table";
import { validationPhases } from "@/lib/validation/tracker";

export default function ValidationsPage() {
  return (
    <div className="space-y-4">
      <section className="border-b border-line pb-6">
        <p className="text-sm font-medium text-accent">Checklist</p>
        <h1 className="mt-2 text-3xl font-semibold">
          Evidence-aware validation tracker
        </h1>
        <p className="mt-4 max-w-4xl text-base leading-7 text-muted">
          The tracker has been converted from unchecked boxes into owner,
          status, and evidence rows. External account tasks remain pending until
          proof is attached.
        </p>
      </section>
      {validationPhases.map((phase) => (
        <ValidationTable key={phase.id} phase={phase} />
      ))}
    </div>
  );
}
