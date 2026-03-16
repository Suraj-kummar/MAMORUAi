import { prisma } from '@/lib/prisma';
import { NextRequest, NextResponse } from 'next/server';

// GET /api/contract/[id] - Get contract details
export async function GET(
    request: NextRequest,
    { params }: { params: { id: string } }
) {
    try {
        const contract = await prisma.contract.findUnique({
            where: { id: params.id },
            include: {
                audits: {
                    orderBy: { createdAt: 'desc' },
                    take: 10
                }
            }
        });

        if (!contract) {
            return NextResponse.json(
                { error: 'Contract not found' },
                { status: 404 }
            );
        }

        return NextResponse.json(contract);
    } catch (error) {
        console.error('Error fetching contract:', error);
        return NextResponse.json(
            { error: 'Failed to fetch contract' },
            { status: 500 }
        );
    }
}

// PUT /api/contract/[id] - Update contract details
export async function PUT(
    request: NextRequest,
    { params }: { params: { id: string } }
) {
    try {
        const body = await request.json();
        const { sourceCode, name, bytecode } = body;

        const contract = await prisma.contract.update({
            where: { id: params.id },
            data: {
                sourceCode,
                name,
                bytecode
            }
        });

        return NextResponse.json(contract);
    } catch (error) {
        console.error('Error updating contract:', error);
        return NextResponse.json(
            { error: 'Failed to update contract' },
            { status: 500 }
        );
    }
}
