import EvidenceUploadForm from '../components/EvidenceUploadForm'

export default function Evidence({ onUploadComplete }) {
  return (
    <main className="mx-auto flex w-full max-w-7xl flex-1 flex-col gap-5 px-4 py-5 sm:px-6 lg:px-8">
      <div className="flex flex-col gap-2">
        <p className="text-sm font-medium uppercase text-slate-500">Fase 3</p>
        <h1 className="text-2xl font-semibold tracking-normal text-ink sm:text-3xl">Subida de evidencia fotografica</h1>
        <p className="max-w-2xl text-sm text-muted">
          Registra una foto asociada a un pedido. El backend guardara la imagen localmente y creara un evento PHOTO_UPLOADED.
        </p>
      </div>

      <EvidenceUploadForm onUploadComplete={onUploadComplete} />
    </main>
  )
}
