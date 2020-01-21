import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(3000, '0.0.0.0', () => {
    console.log('listening on port:', 3000);
    //0919818490
    //
  });
}
bootstrap();
