import { prisma } from '@/lib/prisma';
import { NextRequest, NextResponse } from 'next/server';

// POST /api/scan - Trigger a new security scan
export async function POST(request: NextRequest) {
    try {
        const body = await request.json();
        const { contractAddress, chain = 'ethereum' } = body;

        if (!contractAddress) {
            return NextResponse.json(
                { error: 'Contract address is required' },
                { status: 400 }
            );
        }

        // Validate Ethereum address format
        if (!/^0x[a-fA-F0-9]{40}$/.test(contractAddress)) {
            return NextResponse.json(
                { error: 'Invalid Ethereum address format' },
                { status: 400 }
            );
        }

        // Find or create contract
        let contract = await prisma.contract.findUnique({
            where: { address: contractAddress.toLowerCase() }
        });

        if (!contract) {
            contract = await prisma.contract.create({
                data: {
                    address: contractAddress.toLowerCase(),
                    chain
                }
            });
        }

        // Create audit record
        const audit = await prisma.audit.create({
            data: {
                contractId: contract.id,
                status: 'PENDING'
            }
        });

        // Trigger analysis on the engine
        const engineUrl = process.env.ENGINE_URL || 'http://engine:8000';

        try {
            const response = await fetch(`${engineUrl}/scan`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    contract_address: contractAddress,
                    chain,
                    fetch_source: true,
                    audit_id: audit.id
                })
            });

            if (!response.ok) {
                throw new Error(`Engine returned ${response.status}`);
            }

            // Update audit status to IN_PROGRESS
            await prisma.audit.update({
                where: { id: audit.id },
                data: { status: 'IN_PROGRESS' }
            });

            return NextResponse.json({
                success: true,
                auditId: audit.id,
                contractId: contract.id
            });
        } catch (engineError) {
            console.error('Engine error:', engineError);

            // Mark audit as failed
            await prisma.audit.update({
                where: { id: audit.id },
                data: {
                    status: 'FAILED',
                    summary: 'Failed to connect to analysis engine'
                }
            });

            return NextResponse.json(
                { error: 'Failed to trigger scan on analysis engine' },
                { status: 500 }
            );
        }
    } catch (error) {
        console.error('Error triggering scan:', error);
        return NextResponse.json(
            { error: 'Failed to trigger scan' },
            { status: 500 }
        );
    }
}
