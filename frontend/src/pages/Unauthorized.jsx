export default function Unauthorized() {
  return (
    <main className="mx-auto flex w-full max-w-7xl flex-1 flex-col gap-3 px-4 py-8 sm:px-6 lg:px-8">
      <p className="text-sm font-medium uppercase text-slate-500">403</p>
      <h1 className="text-2xl font-semibold text-ink">Acceso no autorizado</h1>
      <p className="max-w-2xl text-sm text-muted">Tu rol no tiene permisos para abrir esta vista.</p>
    </main>
  )
}
