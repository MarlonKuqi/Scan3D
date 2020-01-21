import { Module } from '@nestjs/common';
import { ObserverGateway } from './observer.gateway';

@Module({
    providers: [ ObserverGateway ],
})
export class ObserverModule {}
