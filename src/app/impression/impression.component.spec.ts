import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImpressionComponent } from './impression.component';

describe('ImpressionComponent', () => {
  let component: ImpressionComponent;
  let fixture: ComponentFixture<ImpressionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ImpressionComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ImpressionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
