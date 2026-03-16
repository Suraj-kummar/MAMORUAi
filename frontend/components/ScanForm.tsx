'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import { Shield, AlertTriangle, CheckCircle, XCircle, Loader2 } from 'lucide-react';

interface ScanFormProps {
    onScanComplete?: (auditId: string) => void;
}

export default function ScanForm({ onScanComplete }: ScanFormProps) {
    const t = useTranslations('dashboard');
    const tErrors = useTranslations('errors');
    const [address, setAddress] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const response = await fetch('/api/scan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    contractAddress: address
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || tErrors('scanFailed'));
            }

            if (onScanComplete && data.auditId) {
                onScanComplete(data.auditId);
            }

            setAddress('');
        } catch (err: any) {
            setError(err.message || tErrors('scanFailed'));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-gradient-to-br from-gray-900 to-black border border-cyan-500/30 rounded-lg p-8 shadow-2xl">
            <div className="flex items-center gap-3 mb-6">
                <Shield className="w-8 h-8 text-cyan-400" />
                <h2 className="text-2xl font-bold text-white">{t('newAudit')}</h2>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <label htmlFor="address" className="block text-sm font-medium text-gray-300 mb-2">
                        {t('contractAddress')}
                    </label>
                    <input
                        id="address"
                        type="text"
                        value={address}
                        onChange={(e) => setAddress(e.target.value)}
                        placeholder={t('enterAddress')}
                        className="w-full px-4 py-3 bg-black/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition-all"
                        disabled={loading}
                        required
                    />
                </div>

                {error && (
                    <div className="flex items-center gap-2 p-3 bg-red-500/10 border border-red-500/30 rounded-lg">
                        <XCircle className="w-5 h-5 text-red-400 flex-shrink-0" />
                        <p className="text-sm text-red-400">{error}</p>
                    </div>
                )}

                <button
                    type="submit"
                    disabled={loading}
                    className="w-full px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white font-semibold rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                    {loading ? (
                        <>
                            <Loader2 className="w-5 h-5 animate-spin" />
                            {t('scanning')}
                        </>
                    ) : (
                        <>
                            <Shield className="w-5 h-5" />
                            {t('triggerAudit')}
                        </>
                    )}
                </button>
            </form>
        </div>
    );
}
