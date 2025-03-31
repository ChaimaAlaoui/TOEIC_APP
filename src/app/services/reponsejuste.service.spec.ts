import { TestBed } from '@angular/core/testing';

import { ReponsejusteService } from './reponsejuste.service';

describe('ReponsejusteService', () => {
  let service: ReponsejusteService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ReponsejusteService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
