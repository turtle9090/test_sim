from sims.models import *

def csv(csv):
    obj = Csv.objects.get(activated=False)
    with open(obj.file_name.path, 'r') as f:
        df = pd.read_csv(f, encoding='latin1', error_bad_lines=False, index_col=False, dtype='unicode',
                         sep=',').replace(np.nan, '', regex=True).replace("\t", '', regex=True)
        df['Due Time\t'] = pd.to_datetime(df['Due Time\t'])
        df['Renewal Time\t'] = pd.to_datetime(df['Renewal Time\t'])
        # print(df)
        row_iter = df.iterrows()
        # for row in row_iter:
        # package_assign, _ = Package.objects.get(name=row[3])
        package_dict = {
            package.name: package for package in Package.objects.all()
        }
        items = []
        for _, row in tqdm(row_iter, total=len(df.index)):
            sing_vsim_data = SingleVSIMData(
                countries_or_region=row['Countries or Regions	'],
                svsim_imsi=row['IMSI	'],
                svsim_iccid=VSIMData.objects.get(vsim_iccid=row['ICCID	']),
                package=package_dict.get(row['Package	']),
                remaining_flow=row['Remaining Flow	'],
                initial_flow=row['Initial Flow	'],
                used_flow=row['Used Flow	'],
                due_time=row['Due Time	'],
                renewal_time=row['Renewal Time	'],
            )
            items.append(sing_vsim_data)
        with SingleVSIMData.objects.bulk_update_or_create_context(
                ['countries_or_region', 'svsim_imsi', 'package', 'initial_flow', 'remaining_flow', 'used_flow',
                 'due_time', 'renewal_time'], match_field='svsim_iccid', batch_size=1000) as bulkit:
            for item in tqdm(items):
                bulkit.queue(item)
        obj.activated = True
        obj.save()
        messages.success(request, 'File upload successful')